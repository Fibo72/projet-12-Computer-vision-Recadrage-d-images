from tkinter import *
import tkinter.messagebox as tkMessageBox

root = Tk()

def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()