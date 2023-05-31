import tkinter as tk
from tkinter import ttk

from GUI.settings import COLOR


style = [{"font":"Arial 13 bold", "borderwidth":3, "relief":"solid", "anchor":"center"},
         {"font":"Arial 13 bold", "borderwidth":3, "relief":"solid", "anchor":"center"},
         {"font":"Arial 10"}, {"font":"Arial 10"}, {}]

packing = [{"fill":"x", "expand":True},
           {"fill":"x", "expand":True},
           {"fill":"x", "expand":True},
           {"fill":"x", "expand":True}]



class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        kw['selectbackground'] = "#b7b7b7"
        kw['selectforeground'] = "#000000"
        tk.Listbox.__init__(self, master,height=3, **kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.bind("<FocusOut>", self.on_focus_out)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i
        self.update_colors()
        self.selection_clear(0,2)
    
    def update_colors(self):
        for i in range(self.size()):
            self.itemconfig(i, {'bg':COLOR[i]})
    
    def on_focus_out(self,event):
        print("focus out")


class SideMenu:
    def __init__(self, master, workspace) -> None:
        self.width = 23
        self.frame = tk.Frame(master, background='#b7b7b7', width=self.width)
        self.widgets = []

        self.workspace = workspace

        self.frame_upper = tk.Frame(self.frame, height = 200, width=self.width)
        self.widgets.append(ttk.Label(self.frame_upper, text="Image list"))
        self.name = tk.Variable()
        self.image_list = tk.Listbox(self.frame_upper, listvariable=self.name, height=3, selectmode="SINGLE") #just like me :(
        self.image_list.bind("<<ListboxSelect>>", self.switch_image)
        self.frame_upper.pack(side="top")
        

        self.frame_lower = tk.Frame(self.frame, height = 200, width=self.width)
        self.widgets.append(ttk.Label(self.frame_lower, text="Points (3 Needed)"))
        self.points_var = tk.Variable(value="1 2 3")
        self.point_list = DragDropListbox(self.frame_lower,listvariable=self.points_var)
        self.frame_lower.pack(side="top", fill="x")

        self.widgets.append(self.image_list)
        self.widgets.append(self.point_list)

        self.pack_all()


    def pack_all(self):
        for i,obj in enumerate(self.widgets):
            obj.config(style[i], background = '#b7b7b7', width=self.width)
            obj.pack(packing[i], side="top", fill="x")
    
    def update_list(self, list_noms):
        list_2 = [" - " + name for name in list_noms]
        self.image_list.configure(height=min(len(list_noms), 40))
        self.name.set(list_2)

    def switch_image(self, event):
        #old_i = self.workspace.current
        #self.workspace.offset[old_i] = [int(self.workspace.canvas.xview()[0]), 
        #                                int(self.workspace.canvas.yview()[0])]
        try:
            self.workspace.current = self.image_list.curselection()[0]
        except:
            pass
        else:
            self.workspace.draw_image()
            self.workspace.canvas.xview_moveto(0)
            self.workspace.canvas.yview_moveto(0)

        
    
    def update_name(self, current, stage):
        if stage == 0:
            self.image_list.itemconfig(current, bg="#b7b7b7")

        elif (stage > 0) and (stage < 3):
            self.image_list.itemconfig(current, bg="yellow")

        elif stage == 3 :
            self.image_list.itemconfig(current, bg="lime green")