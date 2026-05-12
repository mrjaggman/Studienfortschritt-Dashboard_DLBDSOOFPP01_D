"""
Studienziel.py
==============
Ziel: Speichert die persönlichen Studienziele des Studenten.
      Klasse Studienziel aus dem Entity-Klassendiagramm.
      Wird vom Student-Objekt referenziert.

Bibliotheken:
  - Keine externen Bibliotheken nötig
"""


class Studienziel:
    """Speichert die Ziele des Studenten für seinen Studienabschluss."""

    def __init__(self,
                 ziel_abschlussjahr: int,
                 ziel_note: float,
                 pace_wochen_pro_modul: int):

        # Angestrebte Ziele: Jahr des Studienabschlusses, Notendurchschnitt und Bearbeitungsdauer pro Modul
        self.ziel_abschlussjahr: int = ziel_abschlussjahr
        self.ziel_note: float = ziel_note
        self.pace_wochen_pro_modul: int = pace_wochen_pro_modul
