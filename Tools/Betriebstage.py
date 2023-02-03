import sys
from datetime import *
import pandas as pd
import os
from shutil import *
from Tools.btExceptions import *


# gibt das Datum als formatiertes string zurück

def nullstring(dateTime):
    if dateTime is not None and dateTime == 0:
        return "00"
    elif dateTime is not None and dateTime < 10:
        return "0" + str(dateTime)
    elif dateTime is not None:
        return str(dateTime)


# In den unteren beiden Zeilen wird das Date format verändert damit das Endprodukt richtig abgespeichert werden kann

current_day = date.today()
formatted_date = date.strftime(current_day, "%d_%m_%Y")


# Gibt True zurück, wenn es sich um die Fahrtart RB oder RE verwendet

def isRb(zug):
    if zug != "LR RME":
        return True

    if "RB 48" in zug:
        return True
    elif "RE 7" in zug:
        return True
    else:
        return False


# Gibt True zurück, wenn es sich um eine gültige Zeit handelt

def minDiff(start, ende):
    fmt = "%H:%M"

    d1 = datetime.strptime(start[: 5], fmt)

    d2 = datetime.strptime(ende[: 5], fmt)

    ergebnis = (d1 - d2)

    if ergebnis.total_seconds() / 60 < 0 and d2 > d1:
        return True
    elif 20 >= ergebnis.total_seconds() / 60 > 0:
        return False
    elif ergebnis.total_seconds() / 60 > 15 and d2 > d1:
        return True


class Bt:
    def __init__(self, datei, speicherort, art=1):

        self.speicherort = speicherort
        self.path = datei
        self.art = art

        self.t = None
        self.f = None

        if self.art == 1:
            self.t = 1
            self.f = 0

        elif self.art == 0:
            self.t = "ja"
            self.f = "nein"

    def run(self):

        try:

            # In den untern Zeile wird auf dem Default der Ort des gerüst für das Endprodukt gegeben
            default = "pic/StandardTabelle.xlsx"

            # In den unteren Zeilen werden den objekten die speicherorte der übergeben

            copyfile(default, self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")

            df_export_path = self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx"
            df_import_path = self.path
            try:
                df_import = pd.read_excel(df_import_path)
                df_export = pd.read_excel(df_export_path)
            except PermissionError:
                doc_open()
                sys.exit()

            # In der unteren Zeile wird das resultat gespeichert

            copyfile(default, self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")

            # Die untere Schleife sorgt dafür das die leeren stellen in der Tabelle gefüllt werden

            def leereStellen(i):

                if pd.isnull(df_import.loc[i, 'Fahrzeug']):
                    df_import.loc[i, 'Fahrzeug'] = df_import.loc[int(i) - 1, 'Fahrzeug']

                if "<" in df_import.loc[i, 'Fahrzeug'] or ">" in df_import.loc[i, 'Fahrzeug']:
                    df_import.at[i, 'Fahrzeug'] = df_import.at[i, 'Fahrzeug'].replace("<", "")
                    df_import.at[i, 'Fahrzeug'] = df_import.at[i, 'Fahrzeug'].replace(">", "")

                if pd.isnull(df_import.loc[
                                 i, 'Umlaufbezeichnung']):  # Für den seltenen fall ein zug keine Umlaufbezeichnung hat wird der wert 10000 hinzugefügt
                    df_import.loc[index, 'Umlaufbezeichnung'] = 10000

                if pd.isnull(df_import.loc[index, 'Linieninfo']):
                    df_import.loc[index, 'Linie'] = 'LR RME'
                    df_import.loc[index, 'Linieninfo'] = 'LR RME'

            # Die folgende for Schleife sorgt dafür das jedem Fahrzeug erstmal dem wert gefahren = 0 gesetzt wird

            for index, row_export in df_export.iterrows():
                df_export.loc[index, 'Gefahren'] = self.f

            # Die untere for Schleife überprüft pro Fahrzeug, ob in der import Tabelle das Fahrzeug gefahren ist

            for index0, row_export in df_export.iterrows():
                for index1, row_import, in df_import.iterrows():
                    leereStellen(index1)
                    if df_export.at[index0, 'Zug'] in df_import.at[index1, 'Fahrzeug'] and isRb(
                            df_import.at[index1, "Linieninfo"]) and minDiff(df_import.at[index1, "Soll-Abfahrt"],
                                                                            df_import.at[index1, "Soll-Ankunft"]):
                        df_export.loc[index0, 'Gefahren'] = self.t
                        break

            # Wenn dieser Punkt im Programm erreicht wird, wird die neue Tabelle aktualisiert und eine bestätigung wird ausgegeben

            df_export.to_excel(self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")

            fmt = "%Y-%m-%d %H:%M:%S"

            datum = datetime.strptime(str(df_import.loc[20, 'Datum (Soll-Abfahrt)']), fmt)

            os.rename(self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx",
                      self.speicherort + "/" + nullstring(datum.day) + "_" + nullstring(datum.month) + "_" + str(
                          datum.year) +
                      "_Betriebstage.xlsx")

            messagebox.showinfo(title="Erfolg", message="Die Datei wurde erfolgreich abgespeichert")

        except KeyError:
            empty_cell()
            os.remove(self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")

        except FileExistsError:
            os.remove(self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")

        """       except:
                    unkown_error()
                    os.remove(self.speicherort + "/" + str(formatted_date) + "_Betriebstage.xlsx")
         """