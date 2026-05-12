"""
Meilenstein.py
==============
Ziel: Repräsentiert einen Prüfungs- oder Abgabetermin für ein Modul.
      Klasse Meilenstein aus dem Entity-Klassendiagramm.
      Wird von Modulfortschritt verwendet um den Countdown zu berechnen.

Bibliotheken:
  - datetime: Standardbibliothek für Datumsberechnungen
"""

from datetime import date


class Meilenstein:
    """Repräsentiert einen Zieltermin für ein Modul."""

    def __init__(self, faellig_am: date, aktiv: bool = True):
        # Datum bis zu dem das Modul abgeschlossen sein soll
        self.faellig_am: date = faellig_am

        # Aktiv-Flag: False wenn der Meilenstein abgeschlossen oder deaktiviert wurde
        self.aktiv: bool = aktiv

    def tage_bis_faellig(self) -> int:
        """Gibt die Anzahl der verbleibenden Tage bis zum Fälligkeitsdatum zurück."""
        delta = self.faellig_am - date.today()
        return delta.days
