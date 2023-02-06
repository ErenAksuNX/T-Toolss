import tkinter.ttk as ttk


class Entry_with_placeholder(ttk.Entry):

    def __init__(self, placeholder, master, width):
        super().__init__(master, width=width)

        self.state = True  # wenn True ist der Placeholder drinnen, wenn False ist ein Text drinnen

        self.placeholder_style = ttk.Style()
        self.placeholder_style.configure("ph.TEntry", foreground="grey")  # placeholder_style ist der Style der verwendet wird wenn

        self.default_style = ttk.Style()
        self.default_style.configure("df.TEntry")  # default_style ist der Style der verwendet wird, wenn ein Text drinnen steht

        self.placeholder = placeholder

        # Hier werden die Bind gesetzt

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.putPlaceholder()

    # Diese Funktion fügt den Placeholder ein und ändert dementsprechend den Style
    def putPlaceholder(self):
        self.insert(0, self.placeholder)
        self.configure(style="ph.TEntry")

    # Diese Funktion löscht den placeholder und ändert zu dem default style
    def foc_in(self, *args):
        if self.state:
            self.delete('0', 'end')
            self.configure(style="df.TEntry")
            self.state = False

    # Diese Funktion überprüft, ob beim Verlassen des Entrys, ob dies leer ist und fügt dementsprechend den Placeholder ein
    def foc_out(self, *args):
        if not self.get():
            self.putPlaceholder()
            self.state = True
