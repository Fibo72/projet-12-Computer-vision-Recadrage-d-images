import tkinter as tk
from tkinter import Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphViewer:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.title("Graph Viewer")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.fig.add_subplot(111)

    def display_graph(self, x1, y1, x2, y2):
        self.ax.clear()
        self.ax.plot([x1, x2], [y1, y2], 'r-o')
        self.canvas.draw()
        self.window.mainloop()

# Example usage
root = tk.Tk()  # Existing tk.Tk instance
viewer = GraphViewer(root)
viewer.display_graph(1, 1, 2, 3)
