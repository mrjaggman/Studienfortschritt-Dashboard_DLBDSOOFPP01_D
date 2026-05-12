"""
Dashboard.py
============
Ziel: View-Schicht durch Streamlit-Dashboard.
      Zeigt Studienfortschritt, Noten, aktives Modul,
      Countdown und Modulabhängigkeiten als separate Kacheln an.
      Delegiert alle Berechnungen an den Controller (Studienfortschritt).

Bibliotheken:
  - streamlit: Grafische Benutzeroberfläche (Web-Dashboard)
  - plotly.express: Interaktive Diagramme
  - os: Standardbibliothek für Dateipfade
"""

import os
import streamlit as st
import plotly.express as px

from speicher.csv_speicher import CSVSpeicher
from controller.studienfortschritt import Studienfortschritt
from modelle.modul import Ampelfarbe, Lernstatus
from modelle.phasenkonfiguration import Phasenkonfiguration


# --- Seitenkonfiguration ---
st.set_page_config(page_title="Studienfortschritt", layout="wide")

# CSS: Kacheln in derselben Zeile auf gleiche Höhe strecken
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {
    flex: 1;
    display: flex;
    flex-direction: column;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div > div[data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1;
}
</style>
""", unsafe_allow_html=True)

# --- Initialisierung ---
PFAD_CSV = os.path.join(os.path.dirname(__file__), "daten", "module.csv")

# Controller im Session-State speichern damit Aenderungen erhalten bleiben
if "controller" not in st.session_state:
    speicher = CSVSpeicher(PFAD_CSV)
    controller = Studienfortschritt(speicher)
    controller.lade_daten()
    st.session_state.controller = controller

controller = st.session_state.controller

# --- Seitentitel ---
st.title("Dashboard – Studienfortschritt")
st.divider()

# ------------------------------------------------------------
# HAUPTLAYOUT: Linke Seite (breit) + Rechte Seite (schmal)
# ------------------------------------------------------------
col_links, col_rechts = st.columns([2, 1])

# ------------------------------------------------------------
# LINKE SEITE
# ------------------------------------------------------------
with col_links:

    # --- Obere Zeile: Studienfortschritt & Klausurenfrist ---
    kachel1, kachel2 = st.columns([1.2, 1])

    # --- Kachel: Studienfortschritt ---
    with kachel1:
        with st.container(border=True, height=310):
            st.subheader("Studienfortschritt")
            fort = controller.berechne_fortschritt()

            # Fortschrittsbalken mit Prozentwert
            st.markdown(f"Gesamtfortschritt &nbsp;&nbsp;&nbsp; **{fort['prozent']} %**")
            st.progress(fort["prozent"] / 100)

            # Kennzahlen
            m1, m2 = st.columns(2)
            m1.metric("Erreichte ECTS", f"{fort['erreichte_ects']} / {fort['gesamt_ects']}")
            m2.metric("Module", f"{fort['abgeschlossene_module']} / {len(controller.module)}")
            st.caption(
                f"{fort['gesamt_ects'] - fort['erreichte_ects']} ECTS verbleibend · "
                f"{fort['offene_module']} Module offen"
            )
            st.caption("Ziel: Abschluss 2028 · Notendurchschnitt ≤ 2,0")

    # --- Kachel: Nächste Klausurenfrist ---
    with kachel2:
        with st.container(border=True, height=310):
            st.subheader("Nächste Klausurenfrist")
            aktives = controller.get_aktives_modul()

            if aktives is not None:
                mf = controller.get_modulfortschritt(aktives)
                tage = mf.tage_bis_meilenstein()

                if tage is not None:
                    wochen = tage // 7
                    ampel = mf.get_ampelfarbe()
                    if ampel == Ampelfarbe.GRUEN:
                        farbe = "green"
                    elif ampel == Ampelfarbe.GELB:
                        farbe = "orange"
                    else:
                        farbe = "red"

                    st.caption(f"Zieldatum: {aktives.meilenstein_datum}")
                    z1, z2 = st.columns(2)
                    z1.metric("Wochen", wochen)
                    z2.metric("Tage", tage)
                    # Planphase und Restzeit berechnen
                    # Phasenkonfiguration liefert die geplante Dauer pro Phase
                    phasen_config = Phasenkonfiguration()
                    PHASEN_DAUER = phasen_config.als_liste()
                    gesamt_tage = phasen_config.gesamt_tage()
                    vergangen = gesamt_tage - tage         # laut Plan bereits vergangene Tage

                    if vergangen <= 0:
                        # Mehr als 42 Tage bis zum Meilenstein → Modul noch nicht planmäßig gestartet
                        plan_phase_name = "Noch nicht gestartet"
                        plan_info = ""
                    elif vergangen > gesamt_tage:
                        # Meilenstein bereits überschritten
                        plan_phase_name = mf.PHASEN[-1].value
                        ueber = vergangen - gesamt_tage
                        plan_info = f"  \n— {ueber} Tage überzogen"
                    else:
                        # Passende Phase suchen und Resttage in dieser Phase berechnen
                        kumulativ = 0
                        plan_phase_name = mf.PHASEN[-1].value
                        rest_tage = 0
                        for idx, dauer in enumerate(PHASEN_DAUER):
                            kumulativ += dauer
                            if vergangen <= kumulativ:
                                plan_phase_name = mf.PHASEN[idx].value
                                rest_tage = kumulativ - vergangen
                                break
                        if rest_tage > 0:
                            plan_info = f"  \n(noch {rest_tage} Tage bis zur nächsten Phase)"
                        else:
                            plan_info = "  \n(heute letzter Tag)"

                    st.markdown(f":{farbe}[● Pace-Ziel: 5/6 Wochen pro Modul]")
                    st.caption(f"Planphase: **{plan_phase_name}**{plan_info}")
                else:
                    st.info("Kein Meilenstein gesetzt.")
                    neues_datum = st.date_input("Datum setzen", key="datum_input")
                    if st.button("Speichern", key="btn_datum"):
                        controller.setze_meilenstein(aktives, str(neues_datum))
                        del st.session_state.controller
                        st.rerun()
            else:
                st.info("Kein aktives Modul.")

    # --- Kachel: Notenübersicht ---
    with st.container(border=True, height=450):
        st.subheader("Notenübersicht")

        schnitt = controller.berechne_notendurchschnitt()
        typen_schnitt = controller.berechne_durchschnitt_pro_fachbereich()

        # Obere Zeile: grosser Durchschnittswert in eigenem Rahmen
        with st.container(border=True):
            d1, d2 = st.columns([2, 1])
            with d1:
                st.caption("Aktueller Durchschnitt")
            with d2:
                if schnitt is not None:
                    st.markdown(
                        f"<p style='font-size:42px;font-weight:bold;color:#d62728;"
                        f"text-align:right;margin:0;'>{schnitt}</p>",
                        unsafe_allow_html=True
                    )
                else:
                    st.info("Noch keine Noten.")

        # Untere Zeile: Balkendiagramm pro Fachbereich
        st.caption("Durchschnitt pro Fachbereich")
        if typen_schnitt:
            fig = px.bar(
                x=list(typen_schnitt.keys()),
                y=list(typen_schnitt.values()),
                labels={"x": "", "y": "Note"},
                color=list(typen_schnitt.keys()),
                color_discrete_sequence=["#2ca02c", "#1f77b4", "#ff7f0e"],
            )
            # Y-Achse startet bei 0 damit auch Note 1.0 als Balken sichtbar ist
            fig.update_yaxes(range=[0, 4], tickvals=[1, 2, 3, 4], gridcolor="#eeeeee")
            fig.update_layout(
                showlegend=False,
                margin=dict(t=5, b=5, l=0, r=0),
                plot_bgcolor="white",
                height=200,
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Kachel: Modulübersicht ---
    with st.container(border=True, height=700):
        st.subheader("Modulübersicht")

        # Filter-Tabs nach Fachbereich
        alle_fachbereiche = sorted(set(m.fachbereich.value for m in controller.module))
        tabs = st.tabs(["Alle"] + alle_fachbereiche)

        def zeige_module(module_liste):
            for modul in module_liste:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.markdown(f"**{modul.titel}**")
                    c2.caption(f"{modul.ects} ECTS · {modul.pruefungsform.value}")
                    if modul.ist_abgeschlossen():
                        c3.markdown(f":green[Note: {modul.note}]")
                    elif modul.lernstatus is not None:
                        c3.markdown(f":orange[{modul.lernstatus.value}]")
                    else:
                        c3.markdown(":gray[offen]")

        with tabs[0]:
            zeige_module(controller.module)
        for i, fachbereich in enumerate(alle_fachbereiche):
            with tabs[i + 1]:
                zeige_module([m for m in controller.module if m.fachbereich.value == fachbereich])

# ------------------------------------------------------------
# RECHTE SEITE
# ------------------------------------------------------------
with col_rechts:

    # --- Kachel: Aktuelles Modul ---
    with st.container(border=True, height=650):
        st.subheader("Aktuelles Modul")
        aktives = controller.get_aktives_modul()

        if aktives is None:
            st.info("Kein aktives Modul.")
        else:
            mf = controller.get_modulfortschritt(aktives)
            st.markdown(f"**{aktives.titel}**")

            # Badges für ECTS und Prüfungsform
            b1, b2 = st.columns(2)
            b1.markdown(
                f"<span style='background:#e8f4f8;padding:4px 8px;border-radius:4px;"
                f"font-size:13px;'>{aktives.ects} ECTS</span>",
                unsafe_allow_html=True
            )
            b2.markdown(
                f"<span style='background:#e8f4f8;padding:4px 8px;border-radius:4px;"
                f"font-size:13px;'>Prüfungsform: {aktives.pruefungsform.value}</span>",
                unsafe_allow_html=True
            )

            st.divider()

            # Statusanzeige mit nummerierten Phasen
            if mf.status is not None:
                st.markdown(f"Status: :blue[**{mf.status.value}**]")
            st.markdown("")

            for i, phase in enumerate(mf.PHASEN):
                if phase == mf.status:
                    # Aktive Phase: blauer Kreis + fett
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:10px;margin:4px 0;'>"
                        f"<span style='background:#1f77b4;color:white;border-radius:50%;"
                        f"width:26px;height:26px;display:flex;align-items:center;"
                        f"justify-content:center;font-size:12px;font-weight:bold;'>{i+1}</span>"
                        f"<b>{phase.value}</b></div>",
                        unsafe_allow_html=True
                    )
                else:
                    # Inaktive Phase: grauer Kreis
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:10px;margin:4px 0;"
                        f"color:gray;'>"
                        f"<span style='border:2px solid #ccc;border-radius:50%;"
                        f"width:26px;height:26px;display:flex;align-items:center;"
                        f"justify-content:center;font-size:12px;'>{i+1}</span>"
                        f"{phase.value}</div>",
                        unsafe_allow_html=True
                    )

            st.divider()

            # Navigationstasten
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("← Zurück", use_container_width=True):
                    mf.vorherige_phase()
                    controller.aktualisiere_lernstatus(aktives, mf.status)
                    del st.session_state.controller
                    st.rerun()
            with btn2:
                # Wenn letzte Phase erreicht: Neustart-Button statt Weiter-Button
                if mf.status == Lernstatus.ABGEGEBEN:
                    # Neues-Modul-Button ist deaktiviert: Modulauswahl ist eine
                    # bekannte Einschraenkung des Prototyps und wurde bewusst
                    # nicht implementiert um den Rahmen nicht zu sprengen
                    st.button("→ Neues Modul", use_container_width=True, disabled=True)
                elif st.button("Nächste →", use_container_width=True):
                    mf.naechste_phase()
                    controller.aktualisiere_lernstatus(aktives, mf.status)
                    del st.session_state.controller
                    st.rerun()

    # --- Kachel: Modulabhängigkeiten ---
    with st.container(border=True, height=700):
        st.subheader("Modulabhängigkeiten")
        abhaengigkeiten = controller.pruefe_voraussetzungen()

        if not abhaengigkeiten:
            st.info("Keine Abhängigkeiten.")
        else:
            for eintrag in abhaengigkeiten:
                with st.container(border=True):
                    cols = st.columns([4, 1])
                    with cols[0]:
                        st.markdown(f"**{eintrag['modul']}**")
                        st.caption(f"Benötigt: {eintrag['benoetigt']}")
                    with cols[1]:
                        if eintrag["erfuellt"]:
                            st.markdown("✅")
                        else:
                            st.markdown("❌")
