import tkinter as tk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror

from Aymeric.decode_img import prof_topo

class ProfileViewer(tk.Toplevel):
    def __init__(self, master : tk.Tk , toolbar):
        super().__init__(master)
        self.grab_set()
        self.toolbar = toolbar
        self.master = master
        self.title("Graph Viewer")
          
        if self.check_for_points():
            self.initiate_canvas()
            self.display_graph()
        
        else:
            self.destroy()
            showerror("Erreur", "Il faut deux points pour afficher le profil.")

        
    def initiate_canvas(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.fig.add_subplot(111)
    
    def check_for_points(self):        
        if len(self.toolbar.workspace.canvas.ProfileTool.coord_points) == 2:
            canvas = self.toolbar.workspace.canvas
            self.points_list = [canvas.ProfileTool.coord_points[0], 
                                canvas.ProfileTool.coord_points[1]]

            scale = self.toolbar.workspace.scale[self.toolbar.workspace.current]

            self.point_1 = [self.points_list[0][1]//scale, 
                            self.points_list[0][0]//scale]
            
            self.point_2 = [self.points_list[1][1]//scale, 
                            self.points_list[1][0]//scale]
           
            return True
        
        else:
            return False
    
    def display_graph(self):
        self.ax.clear()
        X,Y,Z = prof_topo(self.point_1, self.point_2, self.toolbar.workspace.image_array_list[self.toolbar.workspace.current])
        
        X_arr = np.array(X)
        Y_arr = np.array(Y)

        D = np.sqrt((X_arr - X_arr[0])**2 + (Y_arr - Y_arr[0])**2)
        
        self.ax.plot(D,Z, 'r-')

        self.ax.set_xlabel("Distance")
        self.ax.set_ylabel("Hauteur")
        self.ax.set_title("Profil topographique")
        
        self.canvas.draw()
        self.mainloop()