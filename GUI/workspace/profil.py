from tkinter import *

class Profile:
    def __init__(self, canvas, workspace):
        self.canvas = canvas
        self.workspace = workspace

    def click(self, event):
        if len(self.points) < 2:
            point = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='red', width=2)
            self.points.append(point)
        if len(self.points) == 2:
            self.draw_segment()
        
        else :
            self.active_point = self.find_closest_point(event)

    def move_point(self, event):
        if self.segment is not None and self.active_point is not None:
            self.canvas.coords(self.active_point, event.x-5, event.y-5, event.x+5, event.y+5)
            self.draw_segment()

    def release_point(self, event):
        self.active_point = None

    def draw_segment(self):
        if self.segment is not None:
            self.canvas.delete(self.segment)
        x1, y1, x2, y2 = self.canvas.coords(self.points[0])
        x3, y3, x4, y4 = self.canvas.coords(self.points[1])
        self.segment = self.canvas.create_line(x1+5, y1+5, x3+5, y3+5, fill='blue', width=2)

    def find_closest_point(self, event):
        closest_point = None
        min_distance = float('inf')
        for point in self.points:
            x1, y1, x2, y2 = self.canvas.coords(point)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            distance = ((x_center - event.x) ** 2 + (y_center - event.y) ** 2) ** 0.5
            if distance < min_distance:
                closest_point = point
                min_distance = distance
        return closest_point

    def process(self):
        try :
            point1 = (self.canvas.coords(self.points[0])[0] + 5, self.canvas.coords(self.points[0])[1] + 5)
            point2 = (self.canvas.coords(self.points[1])[0] + 5, self.canvas.coords(self.points[1])[1] + 5)
        except:
            print("Pas assez de points")
        else:
            print(point1, point2) #format : (j, i) = (colonne, ligne)

    def reset(self):
        self.canvas.delete("all")
        self.points = []
        self.segment = None
        self.active_point = None
