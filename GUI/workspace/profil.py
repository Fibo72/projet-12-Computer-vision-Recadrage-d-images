
class Profile:
    def __init__(self, canvas, workspace, toolbar):
        self.canvas = canvas
        self.workspace = workspace
        self.toolbar = toolbar
        self.points = []
        self.coord_points = []
        self.segment = None
        self.active_point = None

    def click(self, mouse_coord, mouse_off):
        x, y = mouse_coord
        if len(self.points) < 2:
            x_off, y_off = mouse_off
            point = self.canvas.create_oval(x_off + x-5, y_off + y-5, x_off + x + 5, y_off + y+5, fill='pink', width=2)
            self.points.append(point)
            self.coord_points.append(mouse_coord)
        if len(self.points) == 2:
            self.draw_segment()
            self.active_point = self.find_closest_point(mouse_coord, mouse_off)
            self.toolbar.toggle_profile("normal")

    def move(self, coord):
        x, y = coord
        if self.active_point is not None:

            x_off, y_off = self.canvas.canvasx(0), self.canvas.canvasy(0)
            self.canvas.coords(self.active_point, x+x_off-3, y+y_off-3, x+x_off+3, y+y_off+3)
            self.draw_segment()

            self.points[self.active_point] = coord


    def release_point(self):
        self.active_point = None

    def draw_segment(self):
        if self.segment is not None:
            self.canvas.delete(self.segment)
        if len(self.points) == 2 :
            try:
                x1, y1, _, _ = self.canvas.coords(self.points[0])
                x3, y3, _, _ = self.canvas.coords(self.points[1])
            except:
                self.points=[]
                self.coord_points=[]
                self.toolbar.toggle_profile("disabled")
                self.draw_segment()
            else:
                self.segment = self.canvas.create_line(x1+5, y1+5, x3+5, y3+5, fill='pink', width=2)

    def find_closest_point(self, mouse_coord, mouse_off):
        closest_point = None
        min_distance = 40
        x_m, y_m = mouse_coord
        x_off, y_off = mouse_off

        for i,point in enumerate(self.points):
            x1, y1, x2, y2 = self.canvas.coords(point)
            x_p = (x1 + x2) / 2
            y_p = (y1 + y2) / 2
            distance = ((x_p - x_off - x_m) ** 2 + (y_p - y_off - y_m) ** 2) ** 0.5
            if (distance < 40) and (distance < min_distance):
                closest_point = self.points[i]
                min_distance = distance
                self.point_number = i
        return closest_point

    def reset(self):
        for _i in range(len(self.points)):
            point_to_delete = self.points.pop(_i)
            self.canvas.delete(point_to_delete)
        if self.segment is not None:
            self.canvas.delete(self.segment)
        self.coord_points = []
        self.segment = None
        self.active_point = None
