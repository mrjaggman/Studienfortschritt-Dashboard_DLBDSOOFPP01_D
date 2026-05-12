"""
Modulfortschritt.py
===================
Ziel: Definiert die Assoziationsklasse Modulfortschritt.
      Verbindet einen Studenten mit einem Modul und speichert
      den Lernfortschritt sowie die Prüfungsleistung.


Bibliotheken:
  - datetime: Standardbibliothek für Datumsberechnungen
"""

from datetime import date, datetime
from modelle.modul import Modul, Lernstatus, Ampelfarbe
from modelle.meilenstein import Meilenstein
from modelle.phasenkonfiguration import Phasenkonfiguration


class Modulfortschritt:
    """
    Assoziationsklasse zwischen Student und Modul.
    Speichert Lernstatus, Note und Meilenstein-Informationen.
    """

    # Reihenfolge der Lernphasen für den Statusworkflow
    PHASEN = [
        Lernstatus.BEGONNEN,
        Lernstatus.SKRIPTBEARBEITUNG,
        Lernstatus.AUFGABENBEARBEITUNG,
        Lernstatus.VERINNERLICHEN,
        Lernstatus.PRUEFUNGSBEREIT,
        Lernstatus.ABGEGEBEN,
    ]

    def __init__(self, modul: Modul, konfiguration: Phasenkonfiguration | None = None):
        # Referenz auf zugehöriges Modul (Aggregation) + Übernahme des Lernstatus aus Modul
        self.modul = modul
        self.status: Lernstatus | None = modul.lernstatus

        # Phasenkonfiguration: Standardwerte wenn keine übergeben wird
        if konfiguration is None:
            konfiguration = Phasenkonfiguration()
        self.konfiguration = konfiguration

        # Meilenstein-Objekt aus dem Datum-String im Modul erstellen. datetine.strptime() konvertiert String zu date-Objekt
        if modul.meilenstein_datum:
            faellig = datetime.strptime(modul.meilenstein_datum, "%Y-%m-%d").date()
            self.meilenstein: Meilenstein | None = Meilenstein(faellig_am=faellig)
        else:
            self.meilenstein = None

        # Finale Note: Wird gesetzt wenn Modul abgeschlossen ist
        self.finale_note: float | None = modul.note

    def naechste_phase(self):
        """Schaltet den Lernstatus eine Phase weiter."""
        if self.status is None:
            self.status = Lernstatus.BEGONNEN
            return
        aktueller_index = self.PHASEN.index(self.status)
        # Nur weiterschalten wenn noch nicht in letzter Phase
        if aktueller_index < len(self.PHASEN) - 1:
            self.status = self.PHASEN[aktueller_index + 1]

    def vorherige_phase(self):
        """Schaltet den Lernstatus eine Phase zurück."""
        if self.status is None:
            return
        aktueller_index = self.PHASEN.index(self.status)
        # Nur zurückschalten wenn nicht in erster Phase
        if aktueller_index > 0:
            self.status = self.PHASEN[aktueller_index - 1]

    def tage_bis_meilenstein(self) -> int | None:
        """Gibt die Anzahl der verbleibenden Tage bis Meilenstein zurück."""
        if self.meilenstein is None:
            return None
        return self.meilenstein.tage_bis_faellig()

    def get_ampelfarbe(self) -> Ampelfarbe | None:
        """
        Berechnet die Ampelfarbe basierend auf verbleibenden Tagen.
        Grün: mehr als 14 Tage, Gelb: 7-14 Tage, Rot: weniger als 7 Tage.
        """
        tage = self.tage_bis_meilenstein()
        if tage is None:
            return None
        if tage > 14:
            return Ampelfarbe.GRUEN
        elif tage >= 7:
            return Ampelfarbe.GELB
        else:
            return Ampelfarbe.ROT

    def ist_abgeschlossen(self) -> bool:
        """Gibt True zurück wenn Modul abgeschlossen wurde."""
        return self.status == Lernstatus.ABGEGEBEN and self.finale_note is not None

    def ist_bestanden(self) -> bool:
        """Gibt True zurück wenn Modul mit einer Note von min. 4.0 bestanden wurde."""
        return self.finale_note is not None and self.finale_note <= 4.0
