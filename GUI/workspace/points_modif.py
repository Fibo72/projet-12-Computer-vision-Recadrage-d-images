increment = {"Right" : (1, 0), "Left" : (-1, 0), "Up" : (0, -1), "Down" : (0, 1)}


class PointsModifier:
    def __init__(self, canvas, workspace):
        self.canvas = canvas
        self.workspace = workspace
        
        self.canvas.bind_all("<Right>", self.move_all_points)
        self.canvas.bind_all("<Left>", self.move_all_points)
        self.canvas.bind_all("<Up>", self.move_all_points)
        self.canvas.bind_all("<Down>", self.move_all_points)

    def click(self, mouse_coord, points_object, mouse_off):
        
        if len(points_object) > 0:
            self.points_object = points_object
            self.active_point = self.find_closest_point(mouse_coord, mouse_off)
    
    def move_all_points(self, event):
        key = event.keysym
        
        
        increment[key]

    def move_point(self, coord):
        x, y = coord
        if self.active_point is not None:

            x_off, y_off = self.canvas.canvasx(0), self.canvas.canvasy(0)
            self.canvas.coords(self.active_point, x+x_off-3, y+y_off-3, x+x_off+3, y+y_off+3)

            coeff = self.workspace.scale[self.workspace.current]

            self.workspace.points[self.workspace.current][self.point_number] = (int((x_off + x) / coeff), int((y_off + y) / coeff))

    def find_closest_point(self, mouse_coord, mouse_off):
        closest_point = None
        min_distance = 10
        x_m, y_m = mouse_coord
        x_off, y_off = mouse_off
        for i,point in enumerate(self.points_object):
            x1, y1, x2, y2 = self.canvas.coords(point)
            x_p = (x1 + x2) / 2
            y_p = (y1 + y2) / 2
            distance = ((x_p - x_off - x_m) ** 2 + (y_p - y_off - y_m) ** 2) ** 0.5
            if (distance < 10) and (distance < min_distance):
                closest_point = self.points_object[i]
                min_distance = distance
                self.point_number = i
        return closest_point

