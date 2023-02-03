import datetime
import os
import tkinter
from tkinter.messagebox import *
import PyPDF2


def save_pdf_file(seiten, name):
    writer = PyPDF2.PdfWriter()

    for file in seiten:
        writer.addPage(file)

    with open(name, "wb") as file_out:
        writer.write(file_out)



def wrong_input():
    showwarning(title="Ungültige Eingabe", message="Bitte überprüfe deine Eingabe!")


# Diese Funktion gibt einen String zurück wo die Nullen für DateTime Elemente hinzugefügt werden

def nullstring(dateTime):
    if dateTime is not None and dateTime == 0:
        return "00"
    elif dateTime is not None and dateTime < 10:
        return "0" + str(dateTime)
    elif dateTime is not None:
        return str(dateTime)


# Diese Funktion entfernt, die doppelte Elemente in einer Liste

def removeDupes(x):
    return list(dict.fromkeys(x))


# Diese Funktion gibt das Datum als String im richtigen Format zurück

def dateFormate_dd_mm_YYYY_HHMMSS(dateTime: datetime):
    dateFormate = nullstring(dateTime.day) + "." + nullstring(dateTime.month) + "." + str(
        dateTime.year) + " " + nullstring(dateTime.hour) + ":" + nullstring(dateTime.minute) + ":" + nullstring(
        dateTime.second)
    return dateFormate


# Diese Funktion cleart den Temp ordner

def clearTemp():
    for file in os.scandir("Temp"):
        try:
            os.remove(file.path)
        except Exception as err:
            showerror("Error!",
                      f"Der Ordner Temp der sich im Programmverzeichnis liegt konnte nicht gelöscht werden \n{str(err)}")


# Diese Funktion löscht die ausgewählte Dateien aus der Listbox

def delete(Lb_PDFFiles: tkinter.Listbox):
    auswahl = Lb_PDFFiles.curselection()

    for i in auswahl[::-1]:
        Lb_PDFFiles.delete(i)


# Diese Funktion cleart die Listbox

def delete_all(Lb_PDFFiles: tkinter.Listbox):
    Lb_PDFFiles.delete(0, tkinter.END)


# Diese Funktion gibt den Index zurück, der im KM-Tool verwendet wird

def getIndex_km(frznr):
    if frznr == 151:
        return 2
    elif frznr == 152:
        return 3
    elif frznr == 153:
        return 4
    elif frznr == 154:
        return 5
    elif frznr == 155:
        return 6
    elif frznr == 156:
        return 7
    elif frznr == 157:
        return 8
    elif frznr == 158:
        return 9
    elif frznr == 159:
        return 10
    elif frznr == 160:
        return 11
    elif frznr == 351:
        return 12
    elif frznr == 352:
        return 13
    elif frznr == 353:
        return 14
    elif frznr == 354:
        return 15
    elif frznr == 355:
        return 16
    elif frznr == 356:
        return 17
    elif frznr == 357:
        return 18
    elif frznr == 358:
        return 19
    elif frznr == 359:
        return 20
    elif frznr == 360:
        return 21
    elif frznr == 361:
        return 22
    elif frznr == 362:
        return 23
    elif frznr == 363:
        return 24
    elif frznr == 364:
        return 25
    elif frznr == 365:
        return 26
    elif frznr == 366:
        return 27
    elif frznr == 367:
        return 28
    elif frznr == 368:
        return 29
    elif frznr == 369:
        return 30
    elif frznr == 370:
        return 31
    elif frznr == 371:
        return 32
    elif frznr == 372:
        return 33
    elif frznr == 373:
        return 34
    elif frznr == 374:
        return 35
    elif frznr == 375:
        return 36
