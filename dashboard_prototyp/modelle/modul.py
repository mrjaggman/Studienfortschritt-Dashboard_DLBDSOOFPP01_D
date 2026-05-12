"""
Modul.py
========
Ziel: Definiert die Klasse Modul und die zugehörigen Enumerationen.
      Repräsentiert einzelnes Studienmodul aus dem Entity-Klassendiagramm.

Bibliotheken:
   - enum: Standardbibliothek für Enumerationen
"""

from enum import Enum


# Definition Enum Klassen
# Setzen feste Wertebereiche (wie in CSV-Datei) und verhindern inkonsistente Eingaben.

class Pruefungsform(Enum):
    KLAUSUR = "Klausur"
    HAUSARBEIT = "Hausarbeit"
    PORTFOLIO = "Portfolio"
    PROJEKTBERICHT = "Projektbericht"
    FALLSTUDIE = "Fallstudie"
    FACHPRAESENTATION = "Fachpraesentation"
    SEMINARARBEIT = "Seminararbeit"
    ADVANCED_WORKBOOK = "Advanced Workbook"
    BACHELORARBEIT = "Bachelorarbeit"
    KOLLOQUIUM = "Kolloquium"


class Modultyp(Enum):
    # Unterscheidung Pflicht- und Wahlpflichtmodule
    PFLICHT = "Pflicht"
    WAHLPFLICHT = "Wahlpflicht"


class Fachbereich(Enum):
    # fachliche Kategorisierung zur Unterstützung der Lernstrategie und Berufsorientierung 
    KI = "KI"
    MATHEMATIK = "Mathematik"
    PROGRAMMIERUNG = "Programmierung"
    GRUNDLAGEN = "Grundlagen"
    ABSCHLUSS = "Abschluss"


class Abschlussstatus(Enum):
    # Modul wurde noch nicht begonnen, bestanden oder nicht bestanden
    OFFEN = "offen"
    BESTANDEN = "bestanden"
    NICHT_BESTANDEN = "nicht_bestanden"


class Lernstatus(Enum):
    # Die sechs Phasen des Statusworkflows aus der Konzeptionsphase
    BEGONNEN = "BEGONNEN"
    SKRIPTBEARBEITUNG = "SKRIPTBEARBEITUNG"
    AUFGABENBEARBEITUNG = "AUFGABENBEARBEITUNG"
    VERINNERLICHEN = "VERINNERLICHEN"
    PRUEFUNGSBEREIT = "PRUEFUNGSBEREIT"
    ABGEGEBEN = "ABGEGEBEN"


class Ampelfarbe(Enum):
    # Zeigt an ob der Student im Zeitplan liegt
    GRUEN = "gruen"
    GELB = "gelb"
    ROT = "rot"


# Def Klasse Modul

class Modul:
    """Repraesentiert ein einzelnes Studienmodul."""

    def __init__(self, modulkuerzel: str, titel: str, ects: int,
                 pruefungsform: Pruefungsform, modultyp: Modultyp,
                 fachbereich: Fachbereich, semester: int,
                 note: float | None = None,
                 benoetigt: str | None = None,
                 lernstatus: Lernstatus | None = None,
                 meilenstein_datum: str | None = None):

        self.modulkuerzel = modulkuerzel
        self.titel = titel

        
        if ects <= 0:
            raise ValueError(f"ECTS muss grösser als 0 sein, erhalten: {ects}")
        self.ects = ects

        self.pruefungsform = pruefungsform
        self.modultyp = modultyp
        self.fachbereich = fachbereich
        self.semester = semester
        self.note: float | None = note
        self.benoetigt: str | None = benoetigt
        self.lernstatus: Lernstatus | None = lernstatus
        self.meilenstein_datum: str | None = meilenstein_datum

    def ist_abgeschlossen(self) -> bool:
        """Gibt True zurück wenn das Modul eine Note hat."""
        return self.note is not None

    def get_abschlussstatus(self) -> Abschlussstatus:
        """Leitet den Abschlussstatus aus der Note ab."""
        if self.note is None:
            return Abschlussstatus.OFFEN
        elif self.note <= 4.0:
            return Abschlussstatus.BESTANDEN
        else:
            return Abschlussstatus.NICHT_BESTANDEN
