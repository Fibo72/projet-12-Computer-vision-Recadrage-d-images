from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel

#VARIABLES
buttons_packing = [{"side":"top"}, {"side":"top"}, {"side":"top"},
                   {"side":"top"}, {"side":"top"}, {"side":"top",  "pady" :20}, {"side":"top"}]


buttons_style = [{"text":"Draw"}, {"text":"Drag"}, {"text":'+'},
                 {"text":'-'}, {"text":'Reset'}, {"text":'Clear', "width": 5}, {"text":'Ruler'}]

COLOR = ['#5669ff','#ff2c64','#42eb00']


#Style
def configure(master: tk.Tk):
    master.configure(bg="#dddddd")
    master.state("zoomed")
    master.title("Rig Hollow")

def style_them_all(button_list):
    for i,button in enumerate(button_list):
        button.configure(buttons_style[i])
        button.configure(state="disabled")

def pack_them_all(button_list):
    for i,button in enumerate(button_list):
        button.pack(buttons_packing[i])


#popup boxes
def show_pop_up(text):
    '''text : string to display'''
    showinfo("Error message", text)

#check right file format

FORMAT = ['.png', '.jpg', '.jpeg', '.dat']

def check_file_format(file_name):
    for ending in FORMAT:
        if file_name.endswith(ending):
            return True
    return False

#process scale rate

def get_scale(h,w,canvas_h,canvas_w):
    '''return scale rate'''
    scale = [min(canvas_h/h[i], canvas_w/w[i]) for i in range(len(h))]
    return scale