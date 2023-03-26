import tkinter as tk
from tkinter import ttk

class DropMenu:
    def __init__(self, master, options, options_fun):
        self.master = master
        self.menu = tk.Menu(self.master, tearoff=False)
        for i,option in enumerate(options):
            self.menu.add_command(label=option, command=options_fun[i])
        self.button = ttk.Button(self.master, text="File", command=self.show_menu)

    def show_menu(self):
        self.menu.post(self.button.winfo_rootx(), self.button.winfo_rooty() + self.button.winfo_height())