import tkinter as tk
from tkinter import ttk

from GUI.settings import COLOR


style = [{"font":"Arial 13 bold", "borderwidth":3, "relief":"solid", "anchor":"center"},
         {"font":"Arial 10"}, {"font":"Arial 10"}]

packing = [{"fill":"x", "expand":True},
           {"fill":"x", "expand":True},
           {"fill":"x", "expand":True}]



class SideMenu:
    def __init__(self, master, workspace) -> None:
        self.width = 23
        self.frame = tk.Frame(master, background='#b7b7b7', width=self.width)
        self.widgets = []

        self.workspace = workspace

        self.frame_upper = tk.Frame(self.frame, height = 200, width=self.width)
        self.widgets.append(ttk.Label(self.frame_upper, text="Images"))
        self.name = tk.Variable()
        self.image_list = tk.Listbox(self.frame_upper, listvariable=self.name, height=3, selectmode="SINGLE") #just like me :(
        self.image_list.bind("<<ListboxSelect>>", self.switch_image)
        self.frame_upper.pack(side="top")
        
        self.widgets.append(self.image_list)

        self.pack_all()


    def pack_all(self):
        for i,obj in enumerate(self.widgets):
            obj.config(style[i], background = '#b7b7b7', width=self.width)
            obj.pack(packing[i], side="top", fill="x")
    
    def update_list(self, list_noms, ref=0):
        list_2 = [ f" {i+1}- {name}" for i,name in enumerate(list_noms)]
        if ref != -1:
            list_2[ref] = " R- " + list_noms[ref]
        else :
            list_2[0] = " R- " + list_noms[0]
        self.image_list.configure(height=min(len(list_noms), 40))
        self.name.set(list_2)

    def switch_image(self, event):
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

        elif (stage > 0) and (stage < self.workspace.maxpoints):
            self.image_list.itemconfig(current, bg="yellow")

        elif stage == self.workspace.maxpoints :
            self.image_list.itemconfig(current, bg="lime green")