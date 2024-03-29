import tkinter as tk

from PIL import Image, ImageTk
from GUI.workspace.canvas import MyCanvas
from GUI.workspace.sidebar import SideBar

class WorkSpace(tk.Frame):
    def __init__(self, master, side_m, toolbar, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.toolbar = toolbar
        self.reinit()
        self.mode = "BLANK"
        
        self.sidebar = SideBar(self, side_m, self.master, background="#b7b7b7")
        self.canvas = MyCanvas(self,self.master, side_m, bg="#dddddd", borderwidth=0, highlightthickness=0)
        self.side_m = side_m

        self.sidebar.update_canvas(self.canvas)

    def display_elements(self):
        self.sidebar.pack(side="left", fill="y")
        self.canvas.grid(row=1, column=1, sticky='nsew')

    def reinit(self):
        self.image_list = []
        self.image_array_list = []
        self.image_tk_list = []
        self.name_list = []
        self.current = 0
        self.ref_image = 0
        self.h = []
        self.w = []
        self.points, self.points_objects = [], []
        self.maxpoints = 3
        self.scale= []
        self.current_image = None
        self.mode = "BLANK"

    def link_to(self, side_m):
        self.canvas.link_side_menu(side_m)
        self.sidebar.link_side_menu(side_m)
        self.side_m = side_m

    def draw_image(self, with_points=True):
        i = self.current

        self.canvas.delete('all')
        w = int(self.w[i] * self.scale[i])
        h = int(self.h[i] * self.scale[i])

        img = self.image_list[i].resize((w, h), resample=Image.Resampling.BOX)
        self.image_tk_list[i] = ImageTk.PhotoImage(img)

        self.current_image = self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk_list[i])
        self.canvas.coords(self.current_image, 0, 0)
        if with_points:
            self.canvas.draw_points()

    def enable_button(self):
        for button in self.sidebar.button_list:
            button.configure(state = "normal")

    def shorten_points(self):
        if len(self.points) > 0:
            for i in range(len(self.points)):
                en_trop = len(self.points[i]) - self.maxpoints
                if en_trop > 0:
                    self.points[i] = self.points[i][:self.maxpoints]
                    for _ in range(en_trop):
                        last = self.points_objects[i].pop()
                        self.canvas.delete(last)
        self.side_m.update_name(self.current, len(self.points[self.current]))
