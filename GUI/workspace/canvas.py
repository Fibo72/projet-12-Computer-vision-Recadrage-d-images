import tkinter as tk
from GUI.settings import *
from GUI.workspace.points_modif import PointsModifier
from GUI.workspace.profil import Profile

class MyCanvas(tk.Canvas):
    def __init__(self, workspace, master, side_m, **kwargs):
        super().__init__(master, **kwargs)
        self.workspace = workspace
        self.side_menu = side_m

        self.ModifTool = PointsModifier(self, self.workspace)
        self.ProfileTool = Profile(self, self.workspace)

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
            if self.workspace.mode == "DRAW" and point_number < self.workspace.maxpoints and self.on_the_image(x,y,i):
                coeff = self.workspace.scale[i]
                x_off, y_off = self.canvasx(0), self.canvasy(0)

                self.workspace.points[i].append((int((x_off + x) / coeff), int((y_off + y) / coeff)))
                self.workspace.points_objects[i].append(self.create_oval(x_off + x - 3,
                                                                        y_off + y - 3,
                                                                        x_off + x + 3, 
                                                                        y_off + y + 3, 
                                                                        fill=COLOR[point_number%3]))
                self.create_text(x_off + x + 10,
                                 y_off + y - 10, 
                                 text = str(point_number + 1), fill=COLOR[point_number%3], font="Arial 12 bold")
                
                self.side_menu.update_name(self.workspace.current, len(self.workspace.points[i]))
            
            elif self.workspace.mode == "DRAG":
                self.drag_on = True
                self.scan_mark(x, y)
                self.drag_start = [x, y]
            
            elif self.workspace.mode == "MODIF":
                x_off, y_off = self.canvasx(0), self.canvasy(0)
                self.ModifTool.click((x,y), self.workspace.points_objects[i], (x_off, y_off))

            elif self.workspace.mode == "PROFILE":
                x_off, y_off = self.canvasx(0), self.canvasy(0)
                self.ProfileTool.click((x,y), (x_off, y_off))
        
    def move(self,event):
        x = event.x
        y = event.y

        if self.workspace.mode == "DRAG" and self.drag_on:
            self.scan_dragto(x, y, gain=1)
        
        elif self.workspace.mode == "MODIF":
            self.ModifTool.move_point((x,y))
        
        elif self.workspace.mode == "PROFILE":
            self.ProfileTool.move((x,y))

    def release(self, event):
        x = event.x
        y = event.y

        if self.workspace.mode == "DRAG" and self.drag_on:
            self.drag_on = False
        
        elif self.workspace.mode == "MODIF":
            self.ModifTool.active_point = None
            self.workspace.draw_image()

        elif self.workspace.mode == "PROFILE":
            self.ProfileTool.release_point()

    def remove_last(self,event=None):
        i = self.workspace.current

        if len(self.workspace.points[i]) > 0:
            last = self.workspace.points_objects[i].pop()
            self.workspace.points[i].pop()
            self.delete(last)
            self.side_menu.update_name(i, len(self.workspace.points[i]))
            self.workspace.draw_image()
    
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
                                                                         fill=COLOR[k%3]))
                self.create_text(-x_off + (x+0.5)*coeff + 10, -y_off + (y+0.5)*coeff - 10, text = str(k+1), fill=COLOR[k], font="Arial 12 bold")

    def hide_points(self):
        i = self.workspace.current
        for point in self.workspace.points_objects[i]:
            self.delete(point)
        self.workspace.points_objects[i] = []
        self.workspace.draw_image(with_points=False)
 
    def on_the_image(self, x, y, i):
        x_t = x + self.canvasx(0)
        y_t = y + self.canvasy(0)
        return (x > 0 and x < self.workspace.w[i] * self.workspace.scale[i] and 
                y > 0 and y < self.workspace.h[i] * self.workspace.scale[i])