import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

class RecadrageMenu(tk.Toplevel):
    def __init__(self, master : tk.Tk , toolbar):
        super().__init__(master)
        self.grab_set()
        self.toolbar = toolbar
        self.master = master
        self.title("Image de référence")
        self.resizable(False, False)

        self.var = tk.StringVar()
        self.var.set("1")

        self.label = ttk.Label(self, text="Image de référence :")
        self.label.pack(pady=10, padx=10)

        button = ttk.Radiobutton(self, text='1ère image', variable=self.var, value="1", command=self.sel, state=tk.ACTIVE)
        button.pack(pady = (0,2))
        button = ttk.Radiobutton(self, text='personnalisé', variable=self.var, value="2", command=self.sel)
        button.pack()
        self.entry = ttk.Entry(self, state=tk.DISABLED, width=5)
        self.entry.pack(pady = (0,2))

        self.button = ttk.Button(self, text="Valider", command=self.close)
        self.button.pack(pady=(10,5))

        self.entry.bind("<Return>", self.close)

    def close(self, event=None):
        if int(self.var.get()) == 1:
            #set ref to 1
            print(1)
            self.destroy()
            print('destroyed')
            #launch recadrage

        else:
            try:
                nb = int(self.entry.get())
            except:
                showinfo("Erreur de donnée", "Entrez un nombre entier.")
            else:
                if nb < 1 or nb > len(self.toolbar.workspace.image_list):
                    showinfo("Erreur de donnée", "Entrez un nombre valide.")
                else :
                    #set ref to nb
                    print(nb)
                    self.destroy()
                    #launch recadrage

    def sel(self):
        if int(self.var.get()) == 1:
            pass
            #disable entry box
            self.entry.config(state=tk.DISABLED)
            #set ref to 1

        elif int(self.var.get()) == 2:
            pass
            #enable entry box
            self.entry.config(state=tk.NORMAL)

