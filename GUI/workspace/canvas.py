import tkinter as tk
from GUI.settings import *

class MyCanvas(tk.Canvas):
    def __init__(self, workspace, master, side_m, **kwargs):
        super().__init__(master, **kwargs)
        self.workspace = workspace
        self.side_menu = side_m

        self.drag_on = False

        self.bind('<Button-1>', self.click)
        self.bind("<B1-Motion>", self.move)
        self.bind('<ButtonRelease-1>', self.release)      
        self.bind_all("<Control-z>", self.remove_last)
    
    def link_side_menu(self, side_m):
        self.side_menu = side_m

    def click(self, event):
        x = event.x
        y = event.y
        i = self.workspace.current
        try:
            point_number = len(self.workspace.points[i])
        except:
            pass
        else:
            if self.workspace.mode == "DRAW" and point_number < 3 and self.on_the_image(x,y,i):
                coeff = self.workspace.scale[i]
                x_off, y_off = self.canvasx(0), self.canvasy(0)

                self.workspace.points[i].append((int((x_off + x) / coeff), int((y_off + y) / coeff)))
                self.workspace.points_objects[i].append(self.create_oval(x_off + x - 3,
                                                                        y_off + y - 3,
                                                                        x_off + x + 3, 
                                                                        y_off + y + 3, 
                                                                        fill=COLOR[point_number]))
                
                self.side_menu.update_name(self.workspace.current, len(self.workspace.points[i]))
            
            elif self.workspace.mode == "DRAG":
                self.drag_on = True
                self.scan_mark(x, y)
                self.drag_start = [x, y]
        

    def move(self,event):
        x = event.x
        y = event.y

        if self.workspace.mode == "DRAG" and self.drag_on:
            self.scan_dragto(x, y, gain=1)
    

    def release(self, event):
        x = event.x
        y = event.y

        if self.workspace.mode == "DRAG" and self.drag_on:
            self.drag_on = False
    

    def remove_last(self,event=None):
        i = self.workspace.current

        if len(self.workspace.points[i]) > 0:
            last = self.workspace.points_objects[i].pop()
            self.workspace.points[i].pop()
            self.delete(last)
            self.side_menu.update_name(self.workspace.current, len(self.workspace.points[i]))
    
    def draw_points(self):
        i = self.workspace.current
        
        if self.workspace.current_image != None:
            self.workspace.points_objects[i] = []
            for k,point in enumerate(self.workspace.points[i]):
                x,y = point
                coeff = self.workspace.scale[i]
                x_off, y_off =  self.coords(self.workspace.current_image)
                
                self.workspace.points_objects[i].append(self.create_oval(-x_off + (x+0.5)*coeff - 3,
                                                                         -y_off + (y+0.5)*coeff - 3,
                                                                         -x_off + (x+0.5)*coeff + 3,
                                                                         -y_off + (y+0.5)*coeff + 3,
                                                                         fill=COLOR[k]))
    
    def on_the_image(self, x, y, i):
        x_t = x + self.canvasx(0)
        y_t = y + self.canvasy(0)
        return (x > 0 and x < self.workspace.w[i] * self.workspace.scale[i] and 
                y > 0 and y < self.workspace.h[i] * self.workspace.scale[i])