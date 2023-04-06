import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askyesno
from Aymeric.decode_img import get_phase_img

from PIL import Image, ImageTk

import os

from GUI.toolbar.drop_menu import DropMenu
from GUI.settings import *

class Toolbar(tk.Frame):
    def __init__(self, master, workspace, side_m):
        super().__init__(master, background="#b7b7b7")
        self.master = master
        self.workspace = workspace
        self.side_m = side_m
        

        file_button = self.initiate_file()
        file_button.button.pack(side="left", padx=(2,0))

        edit_button = self.initiate_edit()
        edit_button.button.pack(side="left", padx=(3,0))

    def update_attributes(self, workspace, side_m):
        self.workspace = workspace
        self.side_m = side_m

    def load_image(self):
        try :
            file_path = filedialog.askopenfilename()
        except:
            pass
        else:
            # Load image
            image_to_display = False

            if file_path.endswith('.dat'):
                self.workspace.reinit()
                self.workspace.image_list.append(Image.fromarray(get_phase_img(file_path)*255, mode='L'))
                self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                self.workspace.h.append(self.workspace.image_list[0].height)
                self.workspace.w.append(self.workspace.image_list[0].width)

                image_to_display = True


            elif check_file_format(file_path):
                self.workspace.reinit()

                self.workspace.image_list.append(Image.open(file_path))
                self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                self.workspace.h.append(self.workspace.image_list[0].height)
                self.workspace.w.append(self.workspace.image_list[0].width)

                image_to_display = True

            if image_to_display:
                self.workspace.points.append([])
                self.workspace.points_objects.append([])


                self.workspace.scale = get_scale(self.workspace.h, self.workspace.w, 
                                                 self.workspace.canvas.winfo_height(), 
                                                 self.workspace.canvas.winfo_width())
                self.side_m.update_list([file_path.split('/')[-1][0:-4]])
                self.workspace.draw_image()
                self.workspace.enable_button()
    
    def load_set(self):
        try:
            dir_path = filedialog.askdirectory()
        except:
            pass
        else:
            name_list = []
            first_image = True
            for j,file_name in enumerate(os.listdir(dir_path)):
                

                file_path = os.path.join(dir_path, file_name)

                if os.path.isfile(file_path):
                    name_list.append(file_name[0:-4])

                    if first_image:
                        self.workspace.reinit()
                        first_image = False

                    if file_path.endswith('.dat'):
                        self.workspace.image_list.append(Image.fromarray(get_phase_img(file_path), mode='L'))
                        self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                        self.workspace.h.append(self.workspace.image_list[j].height)
                        self.workspace.w.append(self.workspace.image_list[j].width)
                        #self.workspace.offset.append([0,0])

                    elif check_file_format(file_path):
                        self.workspace.image_list.append(Image.open(file_path))
                        self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                        self.workspace.h.append(self.workspace.image_list[j].height)
                        self.workspace.w.append(self.workspace.image_list[j].width)
                        #self.workspace.offset.append([0,0])


                    self.workspace.points.append([])
                    self.workspace.points_objects.append([])
            
            if not(first_image):
                self.side_m.update_list(name_list)
                self.workspace.scale = get_scale(self.workspace.h, self.workspace.w,
                                                self.workspace.canvas.winfo_height(),
                                                self.workspace.canvas.winfo_width())
                self.workspace.draw_image()
                self.workspace.enable_button()

    def enable_them_all(self, button_list):
        for button in button_list:
            button.config(state='normal')
    
    def save_points(self):
        print(self.workspace.points)
    
    def initiate_file(self):
        loadings= ["Load Image", "Load Set", "Open Project", "Save"]
        loadings_functions = [self.load_image, self.load_set, self.open_file, self.save_points]

        file_button = DropMenu("File", self, loadings, loadings_functions)
        file_button.button.pack(side="left", padx=(2,0))
        return file_button
    
    def initiate_edit(self):
        loadings= ["Annuler (Ctrl + Z)", "Rétablir (Ctrl + Y)"]
        loadings_functions = [lambda : print("to bind"), lambda : print('to bind')]

        file_button = DropMenu("Edit", self, loadings, loadings_functions)
        file_button.button.pack(side="left", padx=(1,0))
        return file_button
    
    def open_file(self):
        print("to implement")