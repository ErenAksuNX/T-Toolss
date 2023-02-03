from tkinter import messagebox


def unkown_error(err=""):
    messagebox.showerror(title="ERROR", message=f"""NX-0000 Unbekannter Fehler!!
    Melden sie sich mit dem Ausgeführten Betriebstag bei Eren Aksu
    e-mail: eren.aksu@nationalexpress.de\n\n{str(err)}""")


def doc_open(err=""):
    messagebox.showerror(title="ERROR", message=f"NX-0001 Das ausgewählte Dokument ist offen!\n\n{str(err)}")


def empty_cell(err=""):
    messagebox.showerror(title="ERROR", message=f"""NX-0002 Überprüfen sie ob in der ersten Zeile ein Fahrzeug steht,
    oder die Spate \"Linieninfo\" in ihrer Tabelle vorhanden ist\n\n{str(err)}""")


def exists(name="", err=""):
    messagebox.showerror(title="fDatei existiert Bereits",
                         message=f"NX-0003 Es existiert bereits eine Datei mit dem Namen: {name}\n\n{str(err)}")


def vpn_error(err=""):
    messagebox.showerror(title="ERROR!!!", message=f"NX-0004 Datei nicht gefunden überprüfe ob dein VPN an ist !!!\n\n{str(err)}")
