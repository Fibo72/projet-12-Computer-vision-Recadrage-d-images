import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog


class Loading(tk.Toplevel):
    def __init__(self, master, computer):
        super().__init__(master)
        self.grab_set()
        self.master = master
        self.computer = computer

        self.title("Chargement")
        self.resizable(False, False)

        label = ttk.Label(self, text="Calculs en cours...")
        label.pack(pady=10, padx=(5,5))

        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(pady=(0,10), padx=(10,10))

        self.button = ttk.Button(self, text="Enregistrer", command=self.close, state=tk.DISABLED)
        self.button.pack(pady=(0,5))


    def update(self, img_nb, total_img):
        self.progress['value'] = img_nb/total_img*100
    
    def enable_button(self):
        self.button.config(state=tk.NORMAL)
    
    def close(self):
        self.computer.output_dir = filedialog.askdirectory()
        self.destroy()
    