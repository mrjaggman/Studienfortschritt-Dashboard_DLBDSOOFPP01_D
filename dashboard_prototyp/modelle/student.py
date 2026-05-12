"""
Student.py
==========
Ziel: Repräsentiert den Studenten als zentrale Entität des Dashboards.
      Klasse Student aus dem Entity-Klassendiagramm.
      Hält Referenz auf das Studienziel (Assoziation).
      Die Berechnungsmethoden werden im Controller (Studienfortschritt) ausgeführt
      und hier nur als Schnittstelle deklariert (Schichtentrennung).

Bibliotheken:
  - datetime: Standardbibliothek für Datumsberechnungen
"""

from datetime import date
from modelle.studienziel import Studienziel


class Student:
    """Repräsentiert einen eingeschriebenen Studenten."""

    def __init__(self,
                 name: str,
                 matrikelnummer: str,
                 studienbeginn: date,
                 studienziel: Studienziel | None = None):

        self.name: str = name
        self.matrikelnummer: str = matrikelnummer
        self.studienbeginn: date = studienbeginn

        # Studienziel ist optional — kann später gesetzt werden
        self.studienziel: Studienziel | None = studienziel
