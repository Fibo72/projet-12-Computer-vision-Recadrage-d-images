import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from GUI.settings import *
from tkinter.messagebox import askyesno



class SideBar(tk.Frame):
    def __init__(self, workspace, side_m, master, **kwargs):
        super().__init__(workspace, **kwargs)
        self.workspace = workspace
        self.canvas = None
        self.master = master
        self.side_menu = side_m

        self.a = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/draw.png"))
        self.b = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/drag.png"))
        self.c = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/zoom_in.png"))
        self.d = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/zoom_out.png"))
        self.e = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/reset.png"))
        self.f = ImageTk.PhotoImage(Image.open("GUI/workspace/ressources/ruler.png"))

        style = ttk.Style()
        style.configure('TButton', background = '#b7b7b7', borderwidth=0)
        style.map('TButton')

        self.button_list = []
        self.button_list.append(ttk.Button(self.workspace, image=self.a, command=self.draw_toggle))
        self.button_list.append(ttk.Button(self.workspace, image=self.b, command=self.drag_toggle))
        self.button_list.append(ttk.Button(self.workspace, image=self.c, command=self.zoom_in))
        self.button_list.append(ttk.Button(self.workspace, image=self.d, command=self.zoom_out))
        self.button_list.append(ttk.Button(self.workspace, image=self.e, command=self.zoom_reset))
        self.button_list.append(ttk.Button(self.workspace, text="Clear", command=self.clear_points))
        self.button_list.append(ttk.Button(self.workspace, image=self.f, command=lambda :print("no coded yet")))

        style_them_all(self.button_list)
        pack_them_all(self.button_list)
    
    def update_canvas(self, canvas):
        self.canvas = canvas

    def link_side_menu(self, side_m):
        self.side_menu = side_m

    def draw_toggle(self, event=None):
        if self.workspace.mode == "DRAW":
            self.workspace.mode = "BLANK"
        self.master.config(cursor="arrow") # type: ignore
        self.workspace.mode = "DRAW"


    def clear_points(self, event=None):
        if askyesno("Attention","Etes-vous sûr(e) de vouloir supprimer tous les points ?"):
            self.workspace.points[self.workspace.current] = []
            self.workspace.draw_image()
            self.side_menu.update_name(self.workspace.current,0)


    def drag_toggle(self,event=None):
        if self.workspace.mode == "DRAG":
            self.master.config(cursor="arrow") # type: ignore
            self.workspace.mode = "BLANK"
        else:
            self.master.config(cursor="hand2") # type: ignore
            self.workspace.mode = "DRAG"


    def zoom_in(self,event=None):
        if self.workspace.scale[self.workspace.current] <= 2.9 or True:
            self.workspace.scale[self.workspace.current] += 0.2
            self.workspace.draw_image()


    def zoom_out(self,event=None):
        if self.workspace.scale[self.workspace.current] > 0.21:
            self.workspace.scale[self.workspace.current] -= 0.2
            self.workspace.draw_image()


    def zoom_reset(self,event=None):
        i = self.workspace.current
        self.workspace.scale[i] = get_scale([self.workspace.h[i]], [self.workspace.w[i]], 
                                        self.canvas.winfo_height(),   # type: ignore
                                        self.canvas.winfo_width())[0] # type: ignore
        self.workspace.draw_image()
        self.canvas.xview_moveto(0) # type: ignore
        self.canvas.yview_moveto(0) # type: ignore