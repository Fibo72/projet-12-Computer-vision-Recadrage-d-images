import tkinter as tk
from tkinter import filedialog
from Aymeric.decode_img import get_phase_img

from PIL import Image, ImageTk

import os

from GUI.settings import *
from GUI.toolbar.option_menus.menus_handler import MenusHandler
from GUI.toolbar.saveloadhandler import SaveLoadHandler
from GUI.toolbar.drop_menu import DropMenu
from GUI.toolbar.compute.compute import Computer

class Toolbar(tk.Frame):
    def __init__(self, master, workspace, side_m):
        super().__init__(master, background="#b7b7b7")
        self.master = master
        self.workspace = workspace
        self.side_m = side_m

        self.manager = SaveLoadHandler(self)
        self.menuHandler = MenusHandler(self.master, self)
        self.computer = Computer(master)
        
        self.file_button = DropMenu("Fichier", self)
        self.file_button.button.pack(side="left", padx=(1,0))

        self.edit_button = DropMenu("Edition", self)
        self.edit_button.button.pack(side="left", padx=(1,0))

        self.config_button = DropMenu("Configuration", self)
        self.config_button.button.pack(side="left", padx=(1,0))

        self.calcul_button = DropMenu("Calculs", self)
        self.calcul_button.button.pack(side="left", padx=(1,0))


    def link_to(self, workspace, side_m):
        self.workspace = workspace
        self.side_m = side_m

        self.file_button.add_commands(["Nouvelle image", "Nouveau set"],
                                       [self.load_image, self.load_set])
        
        self.edit_button.add_commands(["Annuler (Ctrl + Z)", "Réinitialiser"], #TODO : bind CTRL + Y
                                       [self.workspace.canvas.remove_last,  self.workspace.sidebar.clear_points])
        
        self.config_button.add_commands(["Échelles", "Color Map", "Points"], 
                                        [lambda : print("to bind")]*2 + [self.menuHandler.createPointsMenu])
        
        self.calcul_button.add_commands(["Recadrage", "Profil"], 
                                        [self.menuHandler.createRecadrageMenu]+ [lambda : print("to bind")])


    def load_image(self):
        """
        useful for testint, useless for common use
        """
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
                #TODO: add a line to store the in-meter image
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
                        self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[-1]))
                        self.workspace.h.append(self.workspace.image_list[j].height)
                        self.workspace.w.append(self.workspace.image_list[j].width)
                        #self.workspace.offset.append([0,0])

                    elif check_file_format(file_path):
                        self.workspace.image_list.append(Image.open(file_path))
                        self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[j]))
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
    
    def open_file(self):
        print("to implement")