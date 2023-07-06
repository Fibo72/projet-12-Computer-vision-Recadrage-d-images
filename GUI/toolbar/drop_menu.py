import tkinter as tk
from tkinter import ttk

class DropMenu:
    def __init__(self,text, master):
        self.master = master
        self.menu = tk.Menu(self.master, tearoff=False)
        self.button = ttk.Button(self.master, text=text, command=self.show_menu)

    def add_commands(self, labels, commands):
        for i,option in enumerate(labels):
            self.menu.add_command(label=option, command=commands[i])
        # self.menu.entryconfigure(i, state='disabled')

    def show_menu(self):
        self.menu.post(self.button.winfo_rootx(), self.button.winfo_rooty() + self.button.winfo_height())