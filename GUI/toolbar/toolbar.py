import tkinter as tk

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

        self.manager = None
        self.menuHandler = MenusHandler(self.master, self)
        self.computer = Computer(self)
        self.project_path = None
        
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
        self.manager = SaveLoadHandler(self)

        self.file_button.add_commands(["Nouveau set", "Sauver le projet", "Charger un projet"],
                                       [self.manager.load_set, self.manager.save_project, self.manager.load_project])
        
        self.edit_button.add_commands(["Annuler (Ctrl + Z)", "Réinitialiser"], #TODO : bind CTRL + Y
                                       [self.workspace.canvas.remove_last,  self.workspace.sidebar.clear_points])
        
        self.config_button.add_commands(["Échelles", "Color Map", "Points"], 
                                        [lambda : print("TODO")]*2 + [self.menuHandler.createPointsMenu])
        
        self.calcul_button.add_commands(["Recadrage", "Profil"], 
                                        [self.menuHandler.createRecadrageMenu]+ [self.menuHandler.createProfileMenu])
        self.calcul_button.menu.entryconfig(1, state="disabled")

        self.toggle_profile("disabled")
        self.master.bind("<Control-o>",self.manager.load_project)
        self.master.bind("<Control-s>",self.manager.save_project)


    def toggle_profile(self, state):
        self.calcul_button.menu.entryconfig(1, state=state)
        

    def enable_them_all(self, button_list):
        for button in button_list:
            button.config(state='normal')
