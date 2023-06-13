import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

class RecadrageMenu(tk.Toplevel):
    def __init__(self, master : tk.Tk , toolbar):
        super().__init__(master)
        self.grab_set()
        self.toolbar = toolbar
        self.master = master
        self.title("Recadrage")
        self.resizable(False, False)

        self.label = ttk.Label(self, text="Image de référence :")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self)
        self.entry.pack(padx=50)

        self.button = ttk.Button(self, text="Valider", command=self.close)
        self.button.pack(pady=(10,20))

        self.entry.bind("<Return>", self.close)

    def close(self, event=None):
        try:
            res = int(self.entry.get())
        except:
            showinfo("Erreur de donnée", "Entrez un nombre entier.")
        else:
            if res < 3:
                showinfo("Erreur de donnée", "Entrez un nombre supérieur ou égal à 3.")
            else :
                self.toolbar.workspace.maxpoints = res
                self.toolbar.workspace.shorten_points()
                self.toolbar.workspace.draw_image()
                self.destroy()