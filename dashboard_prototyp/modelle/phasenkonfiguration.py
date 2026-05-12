"""
Phasenkonfiguration.py
======================
Ziel: Speichert die geplante Dauer jeder Lernphase in Tagen.
      Klasse Phasenkonfiguration aus dem Entity-Klassendiagramm.
      Wird von Modulfortschritt verwendet um den Zeitplan zu berechnen.

Bibliotheken:
  - Keine externen Bibliotheken nötig
"""


class Phasenkonfiguration:
    """Speichert die geplante Anzahl Tage pro Lernphase."""

    def __init__(self,
                 phase1_tage: int = 1,
                 phase2_tage: int = 14,
                 phase3_tage: int = 14,
                 phase4_tage: int = 8,
                 phase5_tage: int = 4,
                 phase6_tage: int = 1):

        # Jede Phase hat eine geplante Dauer in Tagen
        # Standardwerte entsprechen dem Pace-Ziel von 42 Tagen (6 Wochen)
        self.phase1_tage = phase1_tage
        self.phase2_tage = phase2_tage
        self.phase3_tage = phase3_tage
        self.phase4_tage = phase4_tage
        self.phase5_tage = phase5_tage
        self.phase6_tage = phase6_tage

    def als_liste(self) -> list[int]:
        """Gibt die Phasendauern als Liste zurück."""
        return [
            self.phase1_tage,
            self.phase2_tage,
            self.phase3_tage,
            self.phase4_tage,
            self.phase5_tage,
            self.phase6_tage,
        ]

    def gesamt_tage(self) -> int:
        """Gibt die Gesamtdauer aller Phasen in Tagen zurück."""
        return sum(self.als_liste())
