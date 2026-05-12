"""
Datenspeicher.py
================
Ziel: Abstrakte Basisklasse für alle Speicherlösungen des Dashboards.
      Jede konkrete Implementierung (z.B. CSVSpeicher) MUSS die
      abstrakten Methoden lade_module() und speichere_module() umsetzen.

Bibliotheken:
  - abc: Standardbibliothek für abstrakte Klassen (kein separater Install nötig)
"""

# abc ist Teil der Python-Standardbibliothek
from abc import ABC, abstractmethod


class Datenspeicher(ABC):
    """Abstrakte Basisklasse für die Datenpersistenz."""

    @abstractmethod
    def lade_module(self) -> list:
        """Lädt alle Module und gibt sie als Liste zurück."""
        pass

    @abstractmethod
    def speichere_module(self, module: list):
        """Speichert eine Liste von Modulen."""
        pass
