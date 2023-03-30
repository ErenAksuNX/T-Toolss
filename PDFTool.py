import os
import shutil
import tkinter.ttk as tk
from tkinter import *
import tkinter.messagebox
from shutil import copyfile
from tkPDFViewer import tkPDFViewer as tkpdf

from Tools.PDFTool import drehen, extrahieren

import tkinter.filedialog

from Tools.HelpFunc import *

from win32api import GetSystemMetrics

from Tools.CustomTkinterWidgets import *


class PDFTool:
    def __init__(self, master):
        self.destination = ""
        self.activeFile = None
        self.master = master

        self.activeMode = ""

        self.master.state('zoomed')
        self.master.minsize(1920, 1080)

        self.fenster_Breite = GetSystemMetrics(0)
        self.fenster_Hoehe = GetSystemMetrics(1)

        print("Die Breite des Fensters beträgt: " + str(self.master.winfo_width()))
        print("Die Höhe des Fensters beträgt: " + str(self.master.winfo_height()))

        self.PDFList = list()

        bgstyle = tk.Style()
        bgstyle.configure(style="new.TFrame", background="#8ec9e9")
        bg2style = tk.Style()
        bg2style.configure(style="My.TFrame", background="#e1e1e1")

        self.PDFWindow()
        self.Buttons()
        self.window()

    def PDFWindow(self):

        self.frame_PDFWindow = tk.Frame(master=self.master, width=640, height=900, style="new.TFrame")
        self.frame_PDFWindow.place(relx=0, rely=1, anchor="sw")

        self.Lb_PDFFiles = Listbox(self.frame_PDFWindow, height=30, selectmode=MULTIPLE, width=50, font=("Arial", 13),
                                   background="#e1e1e1")
        self.Lb_PDFFiles.place(relx=.5, rely=0, anchor="n")

        # PDF Window Buttons

        bt_select = tk.Button(self.frame_PDFWindow, text="Dateien Hinzufügen", command=self.getPDFList, width=25)
        bt_select.place(anchor="n", y=650, relx=.33)

        bt_open = tk.Button(self.frame_PDFWindow, text="Datei Öffnen", command=self.openPDF, width=25)
        bt_open.place(anchor="n", y=700, relx=.33)

        bt_close = tk.Button(self.frame_PDFWindow, text="Datei schließen", width=25, command=self.deleteOld)
        bt_close.place(anchor="n", y=750, relx=.33)

        bt_delete = tk.Button(self.frame_PDFWindow, text="Datei Entfernen",
                              command=lambda: delete(self.Lb_PDFFiles),
                              width=25)
        bt_delete.place(anchor="n", relx=.66, y=650)

        bt_delete_all = tk.Button(self.frame_PDFWindow, text="Alle Dateien entfernen",
                                  command=lambda: delete_all(self.Lb_PDFFiles),
                                  width=25)
        bt_delete_all.place(anchor="n", relx=.66, y=700)

        bt_rename = tk.Button(self.frame_PDFWindow, text="Datei umbenennen", width=25)
        bt_rename.place(anchor="n", relx=.66, y=750)

        en_entry = Entry_with_placeholder(master=self.frame_PDFWindow, placeholder="Neuer Name:", width=50)
        en_entry.place(anchor="n", relx=.5, y=800)

        # endregion PDFWindow

    def Buttons(self):

        self.frame_PDFButtons = tk.Frame(master=self.master, width=640, height=500, style="new.TFrame", borderwidth=2)
        self.frame_PDFButtons.place(anchor="ne", relx=1, rely=0)

        self.img_teilen = PhotoImage(file="pic/bt_PDFTool_Teilen640.png")
        self.img_zusammenfuegen = PhotoImage(file="pic/bt_PDFTool_Zusammenfügen640.png")
        self.img_Start = PhotoImage(file="pic/bt_PDFTool_Start640.png")
        self.img_Save = PhotoImage(file="pic/bt_PDFTool_Save640.png")
        self.img_drehen = PhotoImage(file="pic/bt_PDFTool_drehen640.png")

        bt_extrahieren = tk.Button(self.frame_PDFButtons, image=self.img_teilen,
                                   command=lambda: self.mode("extrahieren"))
        bt_Zusammenfuegen = tk.Button(self.frame_PDFButtons, image=self.img_zusammenfuegen, width=640,
                                      command=lambda: self.mode("zusammenführen"))
        bt_drehen = tk.Button(self.frame_PDFButtons, image=self.img_drehen, command=lambda: self.mode("drehen"))
        bt_Analyse = tk.Button(self.frame_PDFButtons, image=self.img_Start, command=lambda: self.mode("analyse"))
        bt_save = tk.Button(self.frame_PDFButtons, image=self.img_Save, command=lambda: self.mode("save"))

        bt_extrahieren.place(relx=.5, rely=.1, anchor="center")
        bt_Zusammenfuegen.place(relx=.5, rely=.3, anchor="center")
        bt_drehen.place(relx=.5, rely=.5, anchor="center")
        bt_Analyse.place(relx=.5, rely=.7, anchor="center")
        bt_save.place(relx=.5, rely=.9, anchor="center")

        # endregion

    def window(self):

        self.frame_Viewer = tk.Frame(master=self.master, style="new.TFrame", width=640, height=997)

        self.frame_Viewer.place(relx=.5, rely=0, anchor="n")

        # region dreh settings

        self.frame_dreh_settings = tk.Frame(master=self.master, style="new.TFrame", width=640, height=250,
                                            borderwidth=2)

        self.frame_dreh_settings.grid_propagate(False)

        list_grade = ["90", "180", "270"]
        self.sv_grad = StringVar()

        lb_dreh_settings_Seite = tk.Label(master=self.frame_dreh_settings, text="Seite", background="#8ec9e9",
                                          foreground="#0056BF")
        self.en_dreh_settings = tk.Entry(master=self.frame_dreh_settings)
        lb_dreh_settings_um = tk.Label(master=self.frame_dreh_settings, text="um", background="#8ec9e9",
                                       foreground="#0056BF")
        opm_dreh_settings_grad = tk.OptionMenu(self.frame_dreh_settings, self.sv_grad, list_grade[0], *list_grade)
        lb_dreh_settings_drehen = tk.Label(master=self.frame_dreh_settings, text="drehen.", background="#8ec9e9",
                                           foreground="#0056BF")
        bt_dreh_settings_drehen = tk.Button(master=self.frame_dreh_settings, text="Drehen",
                                            command=self.drehen)

        lb_dreh_settings_Seite.grid(row=0, column=0, padx=5, pady=5)
        self.en_dreh_settings.grid(row=0, column=1, pady=5, padx=5)
        lb_dreh_settings_um.grid(row=0, column=2, padx=5, pady=5)
        opm_dreh_settings_grad.grid(row=0, column=3, pady=5, padx=5)
        lb_dreh_settings_drehen.grid(row=0, column=4, padx=5, pady=5)
        bt_dreh_settings_drehen.grid(row=1, column=0, pady=5, padx=5, columnspan=2, sticky="w")

        # endregion

        # region extrahieren settings

        self.frame_extrahieren_settings = tk.Frame(master=self.master, style="new.TFrame", width=640, height=250,
                                                   borderwidth=2)

        lb_extahieren_settings = tk.Label(master=self.frame_extrahieren_settings, background="#8ec9e9",
                                          foreground="#0056BF", text="Seite: ")

        lb_extahieren_settings1 = tk.Label(master=self.frame_extrahieren_settings, background="#8ec9e9",
                                           foreground="#0056BF", text="Extrahieren")

        self.en_extrahieren_settings = tk.Entry(master=self.frame_extrahieren_settings)

        bt_extrahieren_setting = tk.Button(master=self.frame_extrahieren_settings, text="Extrahieren",
                                                command=self.extrahiern)
        self.frame_dreh_settings.grid_propagate(False)

        lb_extahieren_settings.grid(row=0, column=0, padx=5, pady=5)
        self.en_extrahieren_settings.grid(row=0, column=1, padx=5, pady=5)
        lb_extahieren_settings1.grid(row=0, column=2, padx=5, pady=5)
        bt_extrahieren_setting.grid(row=1, column=0, pady=5, padx=5, sticky="w", columnspan=2)

        # endregion

        # region save
        self.frame_save = tk.Frame(master=self.master, style="new.TFrame", width=640, height=250)

        bt_save_dir = tk.Button(master=self.frame_save, text="Speicherverzeichnis wählen", command=self.save_Destination)
        bt_save = tk.Button(master=self.frame_save, text="Speichern", command=self.save)
        bt_save_dir.grid(row=0, column=0, padx=5, pady=5)
        bt_save.grid(row=0, column=1, pady=5, padx=5)
        # end region

    def openPDF(self):

        file = self.getFile()

        self.createView(f"Temp/{file}")
        self.activeFile = f"Temp/{file}"

    def createView(self, file):
        pdfviewer = tkpdf.ShowPdf()
        pdfviewer.destroy()
        self.deleteOld()
        view1 = pdfviewer.pdf_view(width=74, height=50, master=self.frame_Viewer, pdf_location=open(file, "r"))
        view1.pack()

    def deleteOld(self):

        self.activeFile = None

        for widget in self.frame_Viewer.winfo_children():
            widget.destroy()

    # endregion PDFViewer

    def getPDFList(self):
        selectedFiles = tkinter.filedialog.askopenfilenames(title="Wählen sie die PDF Dateien aus",
                                                            filetypes=[("PDF-Datei", "*.pdf"), ("PDF-Datei", "*.PDF"),
                                                                       ("Alle Dateien", "*.*")])

        if not selectedFiles:
            showinfo("Warnung!", "Keine Datei ausgewählt")

        try:
            for file in selectedFiles:
                void, filetype = os.path.splitext(file)
                if filetype != ".pdf":
                    raise Exception("Bitte nur PDF Dateien Auswählen")
                copyfile(file, f"Temp/{os.path.basename(file)}")
                self.PDFList.append(file)
                self.Lb_PDFFiles.insert("end", os.path.basename(file))
        except Exception as err:
            self.PDFList = []
            clearTemp()
            showerror("Fehler!", f"Die Dateien konnten nicht geöffnet werden !!! \n{err} ")
            delete_all(self.Lb_PDFFiles)
            return

    def drehen(self):
        drehen(int(self.sv_grad.get()), int(self.en_dreh_settings.get()), self.activeFile)
        self.openPDF()

    def mode(self, mode):  # Diese Funktion placed die Ausgewählte Frames pro modus

        match mode:
            case "drehen":
                self.frame_dreh_settings.place(anchor="nw", rely=.5, relx=.66)
                self.activeMode = "drehen"

            case "extrahieren":
                self.frame_extrahieren_settings.place(anchor="nw", rely=.5, relx=.66)
                self.activeMode = "extrahieren"

            case "zusammenführen":

                self.activeMode = "zusammenführen"

            case "analyse":

                self.activeMode = "analyse"

            case "save":
                self.frame_save.place(anchor="nw", rely=.5, relx=.66)
                self.activeMode = "save"

        if self.activeMode != "drehen":
            self.frame_dreh_settings.place_forget()
        if self.activeMode != "extrahieren":
            self.frame_extrahieren_settings.place_forget()
        if self.activeMode != "analyse":
            print(1)
        if self.activeMode != "save":
            self.frame_save.place_forget()
        if self.activeMode != "zusammenführen":
            print(1)




    def refresh(self):
        try:
            self.frame_PDFWindow.place_forget()
            self.frame_PDFButtons.place_forget()
            self.frame_Viewer.place_forget()
            self.frame_dreh_settings.place_forget()
            self.frame_dreh_settings.place_forget()
            self.frame_save.place_forget()
        except:
            pass

    def getFile(self):
        cs = self.Lb_PDFFiles.curselection()
        if len(cs) != 1:
            showerror("Fehler", "Bitte genau eine Datei auswählen")
            return ""

        return self.Lb_PDFFiles.get(cs)

    def extrahiern(self):
        newFiles = extrahieren("Temp/" + self.getFile(), self.en_extrahieren_settings.get())

        for file in newFiles:
            self.Lb_PDFFiles.insert(END, file[5:])

    def getFiles(self):
        cs = self.Lb_PDFFiles.curselection()
        files = list()

        for i in cs:
            files.append(self.Lb_PDFFiles.get(i))
        return files

    def save_Destination(self):
        self.destination = tkinter.filedialog.askdirectory(title="Bitte wählen sie den gewünschten Speicherort aus.")

    def save(self):
        if self.destination == "":
            tkinter.messagebox.showwarning(title="Warnung!", message="Bitte wähle einen Speicherort aus.")
            return

        for i in self.getFiles():
            shutil.copyfile(f"temp/{i}", f"{self.destination}/{i}")

        tkinter.messagebox.showinfo("Erfolg", "Die Datei wurde abgespeichert")
