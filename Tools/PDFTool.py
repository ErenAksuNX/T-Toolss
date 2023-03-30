import shutil
import re
import PyPDF2
import os
import tkinter.messagebox
from Exceptions import *

from Tools.HelpFunc import wrong_input, save_pdf_file


def not_allowed_String(string):  # gibt True zurück, wenn der string im gültigen format ist
    string = string.replace(" ", "")
    if not re.match("^[0-9,-]+$", string):
        return True
    return False


def drehen(grad: int, seite: int, file):
    # Die Variable wird um 1 gesenkt da die library anfängt bei 0 zu zählen
    seite = seite - 1

    # Es wird versucht die Data.PDF Datei zu löschen
    if os.path.exists("data/data.pdf"):
        try:
            os.remove("data/data.pdf")
        except:
            tkinter.messagebox.showerror(title="Error!!!", message="Fehler die Data.pdf konnte nicht gelöscht werden ")
    else:
        print("Can not delete the file as it doesn't exists")

    with open(file, "rb") as pdf_in:

        # es werden die reader und die writer erstellt
        reader = PyPDF2.PdfReader(pdf_in)
        writer = PyPDF2.PdfFileWriter()

        # es wird jede Seite von dem Reader in den writer kopiert und dabei wird die ausgewählte seite rotiert
        for i in range(reader.numPages):
            page = reader.getPage(i)

            if i == seite:
                page.rotateClockwise(grad)
            writer.addPage(page)

        # die PDF-Datei wird abgespeichert
        with open("data/data.pdf", "wb") as pdf_out:
            writer.write(pdf_out)

    try:
        os.remove(file)
    except:
        tkinter.messagebox.showerror(title="Error", message="Die Datei konnte nicht richtig gespeichert werden")

    shutil.copyfile("data/data.pdf", file)


def extrahieren(file: str, seite: str):

    # Es wird geprüft, ob überhaupt eine Datei als Parameter übergeben wird
    if file == "":
        tkinter.messagebox.showwarning("Warnung!", "Bitte Wähle eine Gültige datei aus")
        raise NoFileSelected("Keine Datei wurde ausgewählt")

    # Es wird überprüft ob der String gültig ist
    if not_allowed_String(seite):
        tkinter.messagebox.showwarning("Warnung!", "Bitte Wähle eine Gültige datei aus")
        raise Wrong_Pages_Input("Der Eingabe ist nicht gültig")

    # Es werdend die LErzeichen entfernt und die Seiten werden gesplittet
    seite = seite.replace(" ", "")
    seiten = seite.split(",")

    with open(file, "rb") as file_in:
        files = []

        # PDF-Reader
        reader = PyPDF2.PdfReader(file_in)

        # Der Basis name der Datei ohne .pdf
        file_basename = file[:-4]

        # Der Counter wird verwendet, um die PDF-Datei nummeriert abzuspeichern
        counter = 1

        for i in seiten:
            # pages ist der PDF-Writer
            pages = PyPDF2.PdfFileWriter()

            # Falls der User eine Spanne angibt, wird eine Schleife verwendet, um diese Seiten zu extrahieren
            if "-" in i:

                # es wird versucht die Seitenzahlen, als int abzuspeichern
                try:
                    von = int(i.split("-")[0]) - 1
                    bis = int(i.split("-")[1]) - 1
                except ValueError:
                    wrong_input()
                    raise Wrong_Pages_Input("Die Eingabe darf nur folgende Zeichen enthalten (0-9, -, \" \")")

                # es wird geprüft, ob die Pages in einer gültigen Spanne liegen und die Seiten werden mit einer schleife Extrahiert
                if bis + 1 <= reader.numPages:
                    for j in range(von, bis + 1):
                        page = reader.getPage(j)
                        pages.addPage(page)
                else:
                    tkinter.messagebox.showwarning("Warnung!", "Die ausgewählte Seite gibt es nicht in der Datei!")
                    raise Page_Count_To_High()

            elif i.isnumeric():

                # Die Seitenzahl wird als Int gespeichert
                pagenum = int(i) + 1

                # es wird geprüft, ob die Pagenum in der gültigen Spanne liegt
                if pagenum + 1 <= reader.numPages:
                    page = reader.getPage(j)
                    pages.addPage(page)
                else:
                    tkinter.messagebox.showwarning("Warnung!", "Die ausgewählte Seite gibt es nicht in der PDF-Datei!")
                    raise Page_Count_To_High()

            # Es wird geprüft, ob der Dateinamen vergeben ist
            if os.path.exists(f"{file_basename}_{counter}.pdf"):
                if os.path.exists(f"{file_basename}_{counter}___.pdf"):
                    tkinter.messagebox.showwarning("Warnung!", f"Die {counter}te Seite wurde nicht gespeichert da es bereits eine datei mit dem Namen {file_basename}_{counter}.pdf")
                    continue
                output_file = f"{file_basename}_{counter}___.pdf"
            else:
                output_file = f"{file_basename}_{counter}.pdf"

            counter += 1

            with open(output_file, "wb") as file_out:
                pages.write(file_out)

            files.append(output_file)

        return files


"""


    with open(file, "rb") as file_in:

        reader = PyPDF2.PdfReader(file_in)

        file_basename = file[:-4]

        for i in seiten:

            pages = []

            if "-" in i:

                try:
                    von = int(i.split("-")[0]) - 1
                    bis = int(i.split("-")[1]) - 1
                except ValueError:
                    wrong_input()
                    return None

                if bis + 1 <= reader.numPages:
                    for j in range(von, bis):
                        page = reader.getPage(j)
                        pages.append(page)
                else:
                    wrong_input()
                    return None

                save_pdf_file(pages, f"{file_basename}_{counter}.pdf")
                files.append(f"{file_basename}_{counter}.pdf")
                counter = counter + 1

            elif i.isnumeric():

                if int(i) <= reader.numPages:
                    page = reader.getPage(int(i) - 1)
                    pages.append(page)

                else:
                    wrong_input()
                    return None

                save_pdf_file(pages, f"{file_basename}_{counter}.pdf")
                files.append(f"{file_basename}_{counter}.pdf")
                counter = counter + 1

            else:
                wrong_input()
                return None
"""