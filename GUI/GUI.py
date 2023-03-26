import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from PIL import Image, ImageTk

from drop_menu import DropMenu
from settings import *

import os

class ImagePointPicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Frame X")

        self.mode = "BLANK"
        self.image_list = []
        self.image_tk_list = []
        self.current = 0
        self.page_number = tk.StringVar(value='1')

        self.points = []
        self.points_objects = []

        self.scale = [1.0]

        self.drag_on = False
        self.drag_start = [0,0]
        
        # Create the toolbar
        self.toolbar = tk.Frame(self.master)
        self.toolbar.pack(side="top", fill="x")

        # Basic functionnalities
        loadings= ["Load File", "Load Set", "Open", "Save"]
        loadings_functions = [self.load_image, self.load_set] + [lambda : print('hihi')] + [self.save_points]
        file_button = DropMenu(self.toolbar, loadings,loadings_functions)
        file_button.button.pack(side="left", padx=(2,0))

        self.button_list = []
        #Drawing
        self.button_list.append(ttk.Button(self.toolbar, command=self.draw_toggle))
        self.button_list.append(ttk.Button(self.toolbar, command=self.drag_toggle))

        #   Zoom buttons
        self.button_list.append(ttk.Button(self.toolbar, command=self.zoom_in))
        self.button_list.append(ttk.Button(self.toolbar, command=self.zoom_out))
        self.button_list.append(ttk.Button(self.toolbar, command=self.zoom_reset))

        #Clear Button
        self.button_list.append(ttk.Button(self.toolbar, command=self.clear_points))

        #Image nav
        self.button_list.append(ttk.Button(self.toolbar, command=self.go_to_left))
        self.button_list.append(ttk.Entry(self.toolbar, textvariable=self.page_number))
        self.button_list.append(ttk.Button(self.toolbar, command=self.go_to_right))

        style_them_all(self.button_list)
        pack_them_all(self.button_list)
        #Canvas
        self.h, self.w = [], []
        self.canvas = tk.Canvas(self.master, bg="grey",width=1080, height=720)
        self.canvas.pack()

        #Shortcuts bindings
        self.master.bind("<Control-=>", self.zoom_in)
        self.master.bind("<Control-Shift-+>", self.zoom_out)
        self.master.bind("<d>", self.draw_toggle)
        self.master.bind("<g>", self.drag_toggle)
        self.master.bind("<a>", self.zoom_reset)
        self.master.bind("<Control-n>",self.clear_points)
        self.master.bind("<Control-s>",self.save_points)
        self.master.bind("<Return>", self.go_to)


    def init_canvas(self):
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind_all("<Control-z>", self.remove_last)


    def load_image(self):
        file_path = filedialog.askopenfilename()
        self.image_list = []
        self.image_tk_list = []
        self.current = 0

        self.points, self.points_objects = [[]], [[]]

        # Load image
        self.image_list.append(Image.open(file_path))
        self.image_tk_list.append(ImageTk.PhotoImage(self.image_list[0]))

        self.h.append(self.image_list[0].height)
        self.w.append(self.image_list[0].width)

        # Show image on canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.w[0], height=self.h[0])
        self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk_list[0])
        self.canvas.pack()
        self.init_canvas()

        self.mode = "DRAW"
    

    def load_set(self):
        try:
            dir_path = filedialog.askdirectory()
        except:
            pass
        else:
            self.image_list = []
            self.image_tk_list = []
            self.current = 0 

            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)

                if os.path.isfile(file_path):
                    image = Image.open(file_path)

                    self.image_list.append(image)
                    self.image_tk_list.append(ImageTk.PhotoImage(self.image_list[-1]))

                    self.h.append(image.height)
                    self.w.append(image.width)

                    self.points.append([])
                    self.points_objects.append([])
            
            self.scale = [1.0] * len(self.image_list)
            
            # Show 1st image on canvas
            self.canvas.destroy()
            self.canvas = tk.Canvas(self.master, width=self.w[0], height=self.h[0])
            self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk_list[0])
            self.canvas.pack()
            self.init_canvas()

            self.mode = "DRAW"

    def draw_toggle(self, event=None):
        self.master.config(cursor="arrow")
        self.mode = "DRAW"


    def click(self, event):
        x = event.x
        y = event.y
        i = self.current

        if self.mode == "DRAW":
            coeff = self.scale[i]
            x_off, y_off = self.canvas.canvasx(0), self.canvas.canvasy(0)

            self.points[i].append((int((x_off + x) / coeff), int((y_off + y) / coeff)))
            self.points_objects[i].append(self.canvas.create_oval(x_off + x - 3*coeff, y_off + y - 3*coeff,
                                                                  x_off + x + 3*coeff, y_off + y + 3*coeff, 
                                                                  fill='red'))
        
        elif self.mode == "DRAG":
            self.drag_on = True
            self.canvas.scan_mark(x, y)
            self.drag_start = [x, y]
    
    def move(self,event):
        x = event.x
        y = event.y

        if self.mode == "DRAG" and self.drag_on:
            self.canvas.scan_dragto(x, y, gain=1)
    
    def release(self, event):
        x = event.x
        y = event.y

        if self.mode == "DRAG" and self.drag_on:
            self.drag_on = False
            i = self.current
            # [i][1] -= (x - self.drag_start[0])/self.scale[i]
            # [i][0] -= (y - self.drag_start[1])/self.scale[i]

    def remove_last(self,event=None):
        if len(self.points[self.current]) > 0:
            last = self.points_objects[self.current].pop()
            self.points[self.current].pop()
            self.canvas.delete(last)


    def clear_points(self, event=None):
        self.points[self.current] = []
        self.draw_image()


    def save_points(self, event=None):
        print(self.points)


    def drag_toggle(self,event=None):
        self.master.config(cursor="hand2")
        self.mode = "DRAG"


    def zoom_in(self,event=None):
        if self.scale[self.current] <= 2.9:
            self.scale[self.current] += 0.2
            self.draw_image()
            self.draw_points()

    def zoom_out(self,event=None):
        if self.scale[self.current] > 0.21:
            self.scale[self.current] -= 0.2
            self.draw_image()
            self.draw_points()

    def zoom_reset(self,event=None):
        i = self.current
        self.scale[i] = 1

        img = self.image_list[i].resize((self.w[i], self.h[i]))
        self.image_tk_list[i] = ImageTk.PhotoImage(img)

        self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.w[i], height=self.h[i])
        self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk_list[i])
        self.canvas.pack()
        self.init_canvas()

        self.draw_points()


    def go_to_left(self, event=None):
        self.current = (self.current - 1) % len(self.image_list)
        self.page_number.set(str(self.current + 1))
        
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.w[self.current], height=self.h[self.current])
        self.draw_image()
        self.canvas.pack()
        self.init_canvas()

        self.draw_points()
    
    def go_to_right(self, event=None):
        self.current = (self.current + 1) % len(self.image_list)
        self.page_number.set(str(self.current + 1))

        self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.w[self.current], height=self.h[self.current])
        self.draw_image()
        self.canvas.pack()
        self.init_canvas()

        self.draw_points()

    def go_to(self,event=None):
        var = self.page.get()
        try:
            num = int(var)
            valid_input = (num >=1) and (num <= len(self.image_list))
        except:
            valid_input = False
        finally:
            if not(valid_input):
                show_pop_up('page inexistante')
                self.page_number.set(str(self.current + 1))
            else:
                self.page_number.set(str(num))

                self.current = num
                self.page.config(text=str(self.current + 1))

                self.canvas.destroy()
                self.canvas = tk.Canvas(self.master, width=self.w[self.current], height=self.h[self.current])
                self.draw_image()
                self.canvas.pack()
                self.init_canvas()

                self.draw_points()

    def draw_image(self):
        i = self.current

        self.canvas.delete('all')
        w = int(self.w[i] * self.scale[i])
        h = int(self.h[i] * self.scale[i])

        img = self.image_list[i].resize((w, h))
        self.image_tk_list[i] = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk_list[i])


    def draw_points(self):
        i = self.current

        for point in self.points[i]:
            x,y = point
            coeff = self.scale[i]
            x_off, y_off =  [i][0],  [i][1]
            
            self.canvas.create_oval(-x_off + (x-3)*coeff,-y_off + (y-3)*coeff,
                                    -x_off + (x+3)*coeff,-y_off + (y+3)*coeff,
                                    fill='red')

if __name__ == '__main__':
    root = tk.Tk()
    apply_style(root)
    app = ImagePointPicker(root)
    root.mainloop()
