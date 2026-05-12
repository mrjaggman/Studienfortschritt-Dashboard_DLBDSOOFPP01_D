"""
Studienfortschritt.py
=====================
Ziel: Controller-Klasse des Dashboards.
      Koordiniert den Datenzugriff und berechnet Studienfortschritt,
      Notendurchschnitt und aktives Modul.
      Hat keine Kenntnis von der Darstellung (View-Schicht).

Bibliotheken:
  - Keine externen Bibliotheken nötig
"""

from speicher.datenspeicher import Datenspeicher
from modelle.modul import Modul, Lernstatus
from modelle.modulfortschritt import Modulfortschritt


class Studienfortschritt:
    """
    Controller-Klasse: Lädt Daten, berechnet Kennzahlen
    und stellt sie der View-Schicht bereit.
    """

    def __init__(self, datenspeicher: Datenspeicher):
        # Datenspeicher wird von außen übergeben (Aggregation)
        self.datenspeicher = datenspeicher
        # Modulliste wird beim Laden befüllt
        self.module: list[Modul] = []

    def lade_daten(self):
        """Lädt alle Module aus dem Datenspeicher."""
        self.module = self.datenspeicher.lade_module()

    def speichere_daten(self):
        """Speichert den aktuellen Zustand aller Module."""
        self.datenspeicher.speichere_module(self.module)

    def berechne_fortschritt(self) -> dict:
        """
        Berechnet den Studienfortschritt.
        Gibt ein Dictionary mit ECTS, Modulanzahl und Prozent zurück.
        """
        gesamt_ects = sum(m.ects for m in self.module)
        erreichte_ects = sum(m.ects for m in self.module if m.ist_abgeschlossen())
        offene_module = sum(1 for m in self.module if not m.ist_abgeschlossen())
        abgeschlossene_module = sum(1 for m in self.module if m.ist_abgeschlossen())
        prozent = round((erreichte_ects / gesamt_ects) * 100, 1) if gesamt_ects > 0 else 0.0

        return {
            "gesamt_ects": gesamt_ects,
            "erreichte_ects": erreichte_ects,
            "offene_module": offene_module,
            "abgeschlossene_module": abgeschlossene_module,
            "prozent": prozent,
        }

    def berechne_notendurchschnitt(self) -> float | None:
        """Berechnet den gewichteten Notendurchschnitt aller bestandenen Module."""
        bestandene = [m for m in self.module if m.note is not None]
        if not bestandene:
            return None
        gesamt_ects = sum(m.ects for m in bestandene)
        gewichtete_summe = sum(m.note * m.ects for m in bestandene)
        return round(gewichtete_summe / gesamt_ects, 2)

    def berechne_durchschnitt_pro_fachbereich(self) -> dict:
        """Berechnet den Notendurchschnitt pro Fachbereich."""
        fachbereiche = {}
        for m in self.module:
            if m.note is not None:
                fb = m.fachbereich.value
                if fb not in fachbereiche:
                    fachbereiche[fb] = []
                fachbereiche[fb].append(m.note)
        return {fb: round(sum(noten) / len(noten), 2) for fb, noten in fachbereiche.items()}

    def get_aktives_modul(self) -> Modul | None:
        """Gibt das aktuell bearbeitete Modul zurück (hat einen Lernstatus)."""
        for m in self.module:
            if m.lernstatus is not None and not m.ist_abgeschlossen():
                return m
        return None

    def get_modulfortschritt(self, modul: Modul) -> Modulfortschritt:
        """Erstellt ein Modulfortschritt-Objekt für ein gegebenes Modul."""
        return Modulfortschritt(modul)

    def pruefe_voraussetzungen(self) -> list[dict]:
        """
        Prüft für alle Module ob ihre Voraussetzungen erfüllt sind.
        Gibt eine Liste mit Modulname, Voraussetzung und Status zurück.
        """
        bestandene_titel = [m.titel for m in self.module if m.ist_abgeschlossen()]
        ergebnis = []
        for m in self.module:
            if m.benoetigt:
                erfuellt = m.benoetigt in bestandene_titel
                ergebnis.append({
                    "modul": m.titel,
                    "benoetigt": m.benoetigt,
                    "erfuellt": erfuellt,
                })
        return ergebnis

    def aktualisiere_lernstatus(self, modul: Modul, neuer_status: Lernstatus | None):
        """Setzt den Lernstatus eines Moduls und speichert die Änderung."""
        modul.lernstatus = neuer_status
        self.speichere_daten()

    def setze_meilenstein(self, modul: Modul, datum: str):
        """Setzt das Meilenstein-Datum eines Moduls (Format: YYYY-MM-DD)."""
        modul.meilenstein_datum = datum
        self.speichere_daten()
