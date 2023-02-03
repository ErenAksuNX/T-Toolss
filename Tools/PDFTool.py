import shutil
import re
import PyPDF2
import os
import tkinter.messagebox

from Tools.HelpFunc import wrong_input, save_pdf_file

def not_allowed_String(string):
    if not re.match("^[0-9,-]+$", string):
        return True
    return False


def drehen(grad: int, seite: int, file):
    seite = seite - 1

    if os.path.exists("data/data.pdf"):
        try:
            os.remove("data/data.pdf")
        except:
            tkinter.messagebox.showerror(title="Error!!!", message="Fehler die Data.pdf konnte nicht gelöscht werden ")
    else:
        print("Can not delete the file as it doesn't exists")

    with open(file, "rb") as pdf_in:
        reader = PyPDF2.PdfReader(pdf_in)
        writer = PyPDF2.PdfFileWriter()

        for i in range(reader.numPages):
            page = reader.getPage(i)

            if i == seite:
                page.rotateClockwise(grad)
            writer.addPage(page)

        with open("data/data.pdf", "wb") as pdf_out:
            writer.write(pdf_out)

    try:
        os.remove(file)
    except:
        tkinter.messagebox.showerror(title="Error", message="Die Datei konnte nicht richtig gespeichert werden")

    shutil.copyfile("data/data.pdf", file)


def extrahieren(file: str, seite: str):

    if not_allowed_String(seite):
        return None

    files = []
    seite = seite.replace(" ", "")
    seiten = seite.split(",")

    counter = 1

    with open(file, "rb") as file_in:

        reader = PyPDF2.PdfReader(file_in)

        file_basepath = file[:-4]

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

                save_pdf_file(pages, f"{file_basepath}_{counter}.pdf")
                files.append(f"{file_basepath}_{counter}.pdf")
                counter = counter + 1

            elif i.isnumeric():

                if int(i) <= reader.numPages:
                    page = reader.getPage(int(i) - 1)
                    pages.append(page)

                else:
                    wrong_input()
                    return None

                save_pdf_file(pages, f"{file_basepath}_{counter}.pdf")
                files.append(f"{file_basepath}_{counter}.pdf")
                counter = counter + 1

            else:
                wrong_input()
                return None
