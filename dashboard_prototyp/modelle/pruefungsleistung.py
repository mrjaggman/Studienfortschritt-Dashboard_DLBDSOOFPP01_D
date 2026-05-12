"""
Pruefungsleistung.py
====================
Ziel: Repräsentiert das Ergebnis einer abgelegten Prüfung.
      Klasse Pruefungsleistung aus dem Entity-Klassendiagramm.
      Wird von Modulfortschritt referenziert um Prüfungsdaten zu speichern.

Bibliotheken:
  - datetime: Standardbibliothek für Datumsberechnungen
"""

from datetime import date


class Pruefungsleistung:
    """Speichert das Datum und die Note einer abgelegten Prüfung."""

    def __init__(self, datum: date, note: float):
        # Datum der Prüfung/Abgabe und erzielte Note
        self.datum: date = datum
        self.note: float = note
