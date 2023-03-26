from tkinter import ttk
from tkinter.messagebox import showinfo

#VARIABLES
buttons_packing = [{"side":"left"}, {"side":"left"}, {"side":"left", "padx":(20,0)},
                   {"side":"left"}, {"side":"left"}, {"side":"right","padx":(20,0)},
                   {"side":"left", "padx":(20,0)}, {"side":"left"},{"side":"left"},]


buttons_style = [{"text":"Draw", "width":6}, {"text":"Drag", "width":6},
                 {"text":'+', "width":3},
                 {"text":'-', "width":3}, {"text":'Reset'}, { "text":'Clear'},
                 {"text":'<', "width":3}, {"width":3, "justify":"center"},
                 {"text":'>',"width":3}]




#Style
def apply_style(master):
    style = ttk.Style(master)
    style.configure("TButton", bg='red')

def style_them_all(button_list):
    for i,button in enumerate(button_list):
        button.configure(buttons_style[i])

def pack_them_all(button_list):
    for i,button in enumerate(button_list):
        button.pack(buttons_packing[i])

#popup box
def show_pop_up(text):
    '''text : string to display'''
    showinfo("Error message", text)

# All buttons options

#draw_options = {'text' :'Draw', 'command' : self.draw_toggle}
#drag_options = {'text' :'Draw', 'command' : self.drag_toggle}
