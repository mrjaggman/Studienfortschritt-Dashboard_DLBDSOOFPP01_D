"""
CSVSpeicher.py
==============
Ziel: Konkrete Implementierung von Datenspeicher für CSV-Dateien.
      Lädt Moduldaten aus einer CSV-Datei und speichert Änderungen
      (z.B. Lernstatus, Meilenstein) zurück in die Datei.

Bibliotheken:
  - pandas: Datenverarbeitung und CSV-Lesen/Schreiben
  - os: Standardbibliothek für Dateipfade
"""

import os
import pandas as pd
from speicher.datenspeicher import Datenspeicher
from modelle.modul import Modul, Pruefungsform, Modultyp, Fachbereich, Lernstatus


class CSVSpeicher(Datenspeicher):
    """Lädt und speichert Moduldaten aus einer CSV-Datei."""

    def __init__(self, pfad: str):
        # super().__init__() ruft den Konstruktor der abstrakten Elternklasse auf
        super().__init__()
        self.pfad = pfad

    def lade_module(self) -> list:
        """Liest die CSV-Datei und gibt eine Liste von Modul-Objekten zurück."""
        df = pd.read_csv(self.pfad)
        module = []

        for _, zeile in df.iterrows():
            # Wenn Note leer -> None, sonst float-Wert
            note = None if pd.isna(zeile["note"]) else float(zeile["note"])

            # Wenn benoetigt leer -> None, sonst String-Wert
            benoetigt = None if pd.isna(zeile["benoetigt"]) else str(zeile["benoetigt"])

            # Wenn Lernstatus leer -> None, sonst Enum-Wert
            lernstatus = None
            if not pd.isna(zeile["lernstatus"]) and zeile["lernstatus"] != "":
                lernstatus = Lernstatus(zeile["lernstatus"])

            # Wenn Meilenstein-Datum leer -> None, sonst String-Wert
            meilenstein_datum = None
            if not pd.isna(zeile["meilenstein_datum"]) and zeile["meilenstein_datum"] != "":
                meilenstein_datum = str(zeile["meilenstein_datum"])

            # Prüfungsform, Modultyp und Fachbereich als Enum einlesen
            pruefungsform = Pruefungsform(zeile["pruefungsform"])
            modultyp = Modultyp(zeile["modultyp"])
            fachbereich = Fachbereich(zeile["fachbereich"])

            modul = Modul(
                modulkuerzel = zeile["modulkuerzel"],
                titel = zeile["titel"],
                ects = int(zeile["ects"]),
                pruefungsform = pruefungsform,
                modultyp = modultyp,
                fachbereich = fachbereich,
                semester = int(zeile["semester"]),
                note = note,
                benoetigt = benoetigt,
                lernstatus = lernstatus,
                meilenstein_datum = meilenstein_datum,
            )
            module.append(modul)

        return module

    def speichere_module(self, module: list):
        """Schreibt die Liste von Modul-Objekten zurück in die CSV-Datei."""
        zeilen = []
        for m in module:
            zeilen.append({
                "modulkuerzel": m.modulkuerzel,
                "titel": m.titel,
                "ects": m.ects,
                "pruefungsform": m.pruefungsform.value,
                "modultyp": m.modultyp.value,
                "fachbereich": m.fachbereich.value,
                "note": m.note if m.note is not None else "",
                "benoetigt": m.benoetigt if m.benoetigt is not None else "",
                "semester": m.semester,
                "lernstatus": m.lernstatus.value if m.lernstatus is not None else "",
                "meilenstein_datum": m.meilenstein_datum if m.meilenstein_datum is not None else "",
            })

        df = pd.DataFrame(zeilen)
        df.to_csv(self.pfad, index = False)
