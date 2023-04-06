import tkinter as tk
from tkinter.messagebox import askyesno

from GUI.settings import *
from GUI.toolbar.toolbar import Toolbar
from GUI.workspace.workspace import WorkSpace
from GUI.sidemenu.sidemenu import SideMenu

class App:
    def __init__(self, master):
        self.master = master
        configure(self.master)

        #TOOLBAR
        self.toolbar = Toolbar(self.master, None, None)
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky='ew')

        #MAIN PART
        self.workspace = WorkSpace(self.master, None, background="#b7b7b7")
        self.workspace.grid(row=1, column=0, sticky='ns')

        #SIDE MENU
        self.side_menu = SideMenu(self.master, self.workspace)
        self.side_menu.frame.grid(row=1, column=2, sticky='ns')

        self.workspace.link_to_canvas(self.side_menu)
        self.toolbar.update_attributes(self.workspace, self.side_menu)
        
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1, minsize=42)
        root.grid_columnconfigure(1, weight=1000)
        root.grid_columnconfigure(2, weight=1, minsize=50)

        #DISPLAY CONTENT
        self.workspace.display_elements()

        #SHORCUTS BINDING
        self.master.bind("<Control-o>",self.toolbar.open_file)
        self.master.bind("<Control-s>",self.toolbar.save_points)

        self.master.bind("<Control-=>", self.workspace.sidebar.zoom_in)
        self.master.bind("<Control-Shift-+>", self.workspace.sidebar.zoom_out)
        self.master.bind("<d>", self.workspace.sidebar.draw_toggle)
        self.master.bind("<g>", self.workspace.sidebar.drag_toggle)
        self.master.bind("<a>", self.workspace.sidebar.zoom_reset)
        self.master.bind("<Control-n>",self.workspace.sidebar.clear_points)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()