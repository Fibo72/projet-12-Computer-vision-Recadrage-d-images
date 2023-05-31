from tkinter import *

class SegmentDrawer:
    def __init__(self, master):
        self.master = master
        self.test = Canvas(master, width=400, height=400, background="red")
        self.test.pack()
        self.canvas = Canvas(master, width=400, height=400, )
        self.canvas.pack()
        self.points = []
        self.segment = None
        self.active_point = None
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.canvas.bind("<ButtonRelease-1>", self.release_point)

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
        x_center = (x1 + x2 + x3 + x4) / 4
        y_center = (y1 + y2 + y3 + y4) / 4
        self.segment = self.canvas.create_line(x1+2, y1+2, x3+2, y3+2, fill='blue', width=2)
        #self.canvas.create_oval(x_center-3, y_center-3, x_center+3, y_center+3, fill='blue')

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


root = Tk()
app = SegmentDrawer(root)
root.mainloop()
