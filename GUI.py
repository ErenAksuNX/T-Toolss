import subprocess

from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk
from tkinter.filedialog import *
from tkinter.messagebox import *

from Tools import Betriebstage as btt
from Tools.PDFCutter import PDFC
from Tools.Frist import fristhandler
from Tools.km import kmhandler

from Tools.HelpFunc import clearTemp

from PDFTool import PDFTool

from defaults import *


# Abkürzungen
# bt = Betriebstage || Button
# Lb = Listbox
# lb = Label
# opm = Option Menü
# sv = StringVar
# img = image
# bg = background
# en = Entry

def help_window():
    showinfo(title="Hilfe", message="""Bei Problemen melden sie sich bei der folgende e-mail
e-mail: eren.aksu@nationalexpress.de""")


class GUI:
    clearTemp()

    def programmSchliessen(self):
        self.master.destroy()

    def __init__(self, master):

        # region Init vars

        self.bt_dreh_settings_drehen = None
        self.lb_dreh_settings_Seite = None
        self.frame_dreh_settings = None
        self.bt_close = None
        self.Boolean_Dreh = False
        self.bg_logo2 = None
        self.img_logo2 = None
        self.bt_open = None
        self.frame_PDFButtons = None
        self.frame_PDFWindow = None
        self.menu_options = None
        self.menu_help = None
        self.menu_close = None
        self.menubar = None
        self.bt_dateiWaehlen = None
        self.bt_start = None
        self.bg_logo = None
        self.img_logo = None
        self.bt_speicheortWaehlen = None
        self.bg_zug = None
        self.img_zug = None
        self.datei = None
        self.speicherort = None
        self.fullscreenBoolean = False

        # endregion Init vars

        self.master: Tk = master

        self.GUILayout()

        self.sv_Tools = StringVar()
        self.sv_bt = StringVar()

        self.paddings = {'padx': 5, 'pady': 5}

        self.options = ['Betriebstage-Tool', 'Kilometerstand-Tool', 'Auswertung Fristeinhaltung', 'PDF Cutter']

        # In den unteren Zeilen wird das Dropdown Menü für die ausgabe von dem BT Tool Erstellt
        self.btt_options = ["1/0", "ja/nein"]
        self.opm_bt = tk.OptionMenu(self.master, self.sv_bt, self.btt_options[1], *self.btt_options)
        self.lb_bt_auswahltext = tk.Label(self.master, text="Ausgabe: ")

        # In dem unteren Teil wird das DD Menü erstellt, womit man das Tool was man verwenden will auswählen kann
        self.lb_auswahltext = tk.Label(self.master, text="Tool: ")
        self.opm_Tools = tk.OptionMenu(self.master, self.sv_Tools, self.options[0], *self.options,
                                       command=self.refresh)

        # Hier wird das Label erstellt, womit man die Anleitung öffnen kann
        self.lb_anleitung = tk.Label(self.master, text="Drücke hier für die Anleitung", foreground="#0056a4",
                                     anchor="ne")

        # In dem restlichen Code werden nur noch die einzelnen Komponenten geplaced
        self.lb_auswahltext.place(anchor="nw", x=5, y=5)
        self.opm_Tools.place(anchor="nw", x=40, y=5)
        self.bt_ausgabe()

        # Bei den Labels wird ein Hintergrund gegeben, weil sie sonst einen weißen Hintergrund haben #8ec9e9 ist das NX Baby blau
        self.lb_anleitung.config(background=NX_BACKGROUND_COLOR)
        self.lb_bt_auswahltext.config(background=NX_BACKGROUND_COLOR)
        self.lb_auswahltext.config(background=NX_BACKGROUND_COLOR)

    def buttons(self):

        self.removeButtons()

        self.bt_dateiWaehlen.place(anchor=CENTER, relx=.5, rely=.2)
        self.bt_speicheortWaehlen.place(anchor=CENTER, relx=.5, rely=.5)
        self.bt_start.place(anchor=CENTER, relx=.5, rely=.8)

    def GUILayout(self):
        # Hier wird der Header designt
        self.master.title("National Express Technik-Tool")
        self.master.iconbitmap("pic/national-express.ico")

        self.master.geometry("500x500")
        self.master.minsize(500, 500)

        # Shortcuts für den Fullscreen
        self.master.bind("<F11>", self.fullscreen)
        self.master.bind("<Escape>", self.closeFullscreen)

        # Hier wird der BG hinzugefügt
        self.master.config(background=NX_BACKGROUND_COLOR)

        self.img_zug = PhotoImage(file="data/zuege_freigestellt.png")
        self.bg_zug = Label(self.master, image=self.img_zug, background=NX_BACKGROUND_COLOR, anchor="sw")
        self.bg_zug.place(relx=.0, rely=1.0, anchor="sw")

        self.img_logo = PhotoImage(file="pic/natex_stacked_png.png")
        self.bg_logo = Label(self.master, image=self.img_logo, background=NX_BACKGROUND_COLOR, anchor='se')
        self.bg_logo.place(rely=1, relx=1, anchor='se')

        # Hier werden die Buttons erstellt, womit man Die Dateien wählen kann einen speicherort wählen kann und das Programm starten kann
        self.bt_dateiWaehlen = tk.Button(self.master, text="Datei Wählen", command=self.getPath)
        self.bt_speicheortWaehlen = tk.Button(self.master, text="Speicherort Wählen", command=self.getSavePath)
        self.bt_start = tk.Button(self.master, text="Programm Starten", command=self.start)

        self.Menu()
        self.buttons()

    def Menu(self):
        # im unteren Teil wird das Menü Designet
        self.menubar = Menu(self.master)

        self.menu_close = Menu(self.menubar)
        self.menu_close.add_command()

        self.menubar = Menu(self.master)

        self.menu_Programm = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_Programm, label="Programm")

        self.menu_close = Menu(self.menu_Programm)
        self.menu_Programm.add_cascade(label="Programm schließen", command=self.programmSchliessen)

        self.menu_fullscreen = Menu(self.menu_Programm)
        self.menu_Programm.add_command(label="Vollbild", command=self.fullscreen)

        self.menu_options = Menu(self.menubar)
        self.menu_options.add_command(label="Betriebstage Tool Ausgabe", command=self.bt_ausgabe)

        self.menu_help = Menu(self.menubar)

        self.menubar.add_cascade(label="Optionen", menu=self.menu_options)
        self.menubar.add_cascade(label="Hilfe", command=help_window)

        self.master.config(menu=self.menubar)

    # region Fullscreen

    def fullscreen(self, x=None):

        print(x)

        self.fullscreenBoolean = not self.fullscreenBoolean
        self.master.attributes("-fullscreen", self.fullscreenBoolean)

    def closeFullscreen(self, x):

        print(x)

        self.master.attributes("-fullscreen", False)
        self.fullscreenBoolean = False

    # endregion

    def start(self):
        # in den Variablen wird die Auswahl vom DD Menü gespeichert

        cmd = self.sv_Tools.get()
        bttype = self.sv_bt.get()

        # Hier wird überprüft ob der User auch Datei und Speicherort ausgewählt hat

        if self.datei is None:
            messagebox.showerror(title="Keine Datei ausgewählt", message="Bitte wählen sie eine Datei aus")
            return
        elif self.speicherort is None:
            messagebox.showerror(title="Kein Speicherort ausgewählt", message="Bitte wählen sie speicherort aus ")
            return

        # hier wird der Parameter erstellt, was die Ausgabe vom BT Tool Bestimmt

        if bttype == "ja/nein":
            bt_type = 0
        else:
            bt_type = 1

        # Hier wird überprüft welches Tool der User ausgewählt hat und der dem entsprechenden Code wird ausgeführt

        # Betriebstage Tool

        if cmd == self.options[0]:
            bt = btt.Bt(self.datei, self.speicherort, bt_type)
            bt.run()

            # PDFCutter

        elif cmd == self.options[3]:

            self.removeButtons()

            for file in self.datei:
                pdf = PDFC.PDF(file, self.speicherort)
                pdf.start()

            # Fristen einhaltung

        elif cmd == self.options[2]:
            frist = fristhandler.FristHandler(self.datei, self.speicherort)
            frist.run()

        elif cmd == self.options[1]:
            km = kmhandler.Km(self.datei, self.speicherort)
            km.run()

    def getPath(self):
        cmd = self.sv_Tools.get()
        path = None

        # in dieser Funktion wir der Filedialog für das ausgewählte Tool ausgewählt

        if cmd == self.options[0]:

            path = askopenfilename(title="Bitte wählen sie die Excel-Datei aus",
                                   filetypes=[("Excel-Datei", "*.xlsx"), ("Alle Dateien", "*.*")])
        elif cmd == self.options[3]:
            path = askopenfilenames(title="Wählen sie bitte die PDF Datei aus die sie Cutten wollen.",
                                    filetypes=[("PDF-Datei", "*.pdf"), ("Alle Dateien", "*.*")])

        elif cmd == self.options[2]:
            path = askopenfilename(title="Bitte wählen sie die IH-Vorschläge Excel Datei aus.",
                                   filetypes=[("Excel-Datei", "*.xlsx"), ("Alle Dateien", "*.*")])

        elif cmd == self.options[1]:
            path = askopenfilename(title="Bitte wählen sie die Excel-Tabelle mit dem Rail-Cloud auszug aus.",
                                   filetypes=[("Excel-Datei", "*.xlsx"), ("Alle Dateien", "*.*")])

        self.datei = path

        if path == "":
            messagebox.showinfo(title="Keine Datei Ausgewählt!!!", message="Bitte wählen sie eine Datei aus")

    def getSavePath(self):
        path = askdirectory()
        self.speicherort = path

        if path == "":
            messagebox.showinfo(title="Keine Speicherort ausgewählt !!!",
                                message="Bitte wählen sie ein Speicheort aus !")

    def refresh(self, value):
        if value is not self.options[0]:
            self.lb_bt_auswahltext.place_forget()
            self.opm_bt.place_forget()
            self.lb_anleitung.place_forget()

        if value == self.options[1]:
            self.km_ausgabe()

        if value == self.options[0]:
            self.bt_ausgabe()

        if value == self.options[3]:
            self.pdfTool()
        else:
            self.buttons()
            self.master.minsize(500, 500)
            self.master.geometry("500x500")
            self.master.state("normal")

            self.pdftool.refresh()

    def pdfTool(self):

        try:
            self.frame_PDFWindow.place_forget()
            self.frame_PDFButtons.place_forget()
        except:
            pass

        self.removeButtons()
        self.pdftool = PDFTool(self.master)

    def km_ausgabe(self):

        self.lb_anleitung.place(relx=1, rely=0, anchor="ne")
        self.lb_anleitung.bind("<Button-1>",
                               lambda: subprocess.Popen(["pic/Kilometer-Tool Anleitung.pdf"], shell=True))

    def bt_ausgabe(self):

        self.lb_anleitung.place(relx=1, rely=0, anchor="ne")
        self.opm_bt.place(x=40, y=30, anchor="nw")
        self.lb_anleitung.bind("<Button-1>",
                               lambda: subprocess.Popen(["pic/Betriebstage-Tool Anleitung.pdf"], shell=True))

    def anleitung(self):
        # diese Funktion ändert die Anleitungsdatei, die sich öffnet
        tool = self.sv_Tools.get()

        if tool == self.options[0]:
            subprocess.Popen(["pic/Betriebstage-Tool Anleitung.pdf"], shell=True)
        elif tool == self.options[1]:
            subprocess.Popen(["pic/Kilometer-Tool Anleitung.pdf"], shell=True)

    def removeButtons(self):
        # Die Buttons werden entfernt
        self.bt_start.place_forget()
        self.bt_dateiWaehlen.place_forget()
        self.bt_speicheortWaehlen.place_forget()
