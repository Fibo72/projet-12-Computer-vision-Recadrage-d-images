from Aymeric.decode_img import get_img
from tkinter import filedialog
from tkinter.messagebox import showwarning, showinfo
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk
from GUI.settings import check_file_format, get_scale
from GUI.settings import format_points
import os
import numpy as np
import json

class SaveLoadHandler():
    def __init__(self, toolbar) -> None:
        self.toolbar = toolbar
        self.workspace = toolbar.workspace
        self.side_m = toolbar.side_m
        self.origin_path = None
    
    def link(self, workspace, side_m):
        self.workspace = workspace
        self.side_m = side_m

    def load_set(self, path=None):
        """
        Loads a set of .dat images localized in a single folder
        """
        try:
            if path is None:
                dir_path = filedialog.askdirectory()
                self.origin_path = dir_path
            else:
                dir_path = path
                self.origin_path = dir_path
        except:
            pass
        else:
            name_list = []
            first_image = True
            for j,file_name in enumerate(os.listdir(dir_path)):
                

                file_path = os.path.join(dir_path, file_name)

                if os.path.isfile(file_path):
                    name_list.append(file_name[0:-4])

                    if file_path.endswith('.dat'):
                        self.workspace.name_list.append(file_name)
                        if first_image:
                            self.workspace.reinit()
                            first_image = False
                            
                        self.workspace.image_list.append(Image.fromarray(get_img(file_path, type="phase"), mode='L'))
                        self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                        self.workspace.h.append(self.workspace.image_list[j].height)
                        self.workspace.w.append(self.workspace.image_list[j].width)

                    # elif check_file_format(file_path):
                    #     self.workspace.image_list.append(Image.open(file_path))
                    #     self.workspace.image_tk_list.append(ImageTk.PhotoImage(self.workspace.image_list[0]))
                    #     self.workspace.h.append(self.workspace.image_list[j].height)
                    #     self.workspace.w.append(self.workspace.image_list[j].width)


                    self.workspace.points.append([])
                    self.workspace.points_objects.append([])
            
            if not(first_image):
                self.side_m.update_list(name_list)
                self.workspace.scale = get_scale(self.workspace.h, self.workspace.w,
                                                self.workspace.canvas.winfo_height(),
                                                self.workspace.canvas.winfo_width())
                self.workspace.draw_image()
                self.workspace.enable_button()

    def save_project(self):
        """
        Saves a project in a JSON file among others, it will save
            - path of the images (the JSON is loded in the same folder)
            - points on each images
        """
        dir_path = filedialog.askdirectory()
        img_dict = {}
        try:
            img_dict["p1"] = np.array(self.workspace.points).tolist()
        except:
            showwarning("Attention","Toutes les images n'ont pas le même nombre de points")
        else:
            img_dict["img_name"] = self.workspace.name_list

            dict = {}
            dict["img_dict"] = img_dict
            dict["crop_number"] = 0     #TODO : add crop number
            dict["origin_path"] = self.origin_path
            dict["out_path"] = dir_path
            dict["comment"] = "comment here"

            with open(os.path.join(dir_path, "project.json"), 'w') as f:
                json.dump(dict, f, indent=4)

            self.toolbar.project_path = os.path.join(dir_path, "project.json")
            showinfo("Succès","Projet sauvegardé avec succès")

    def load_project(self):
        """
        Loads a project previously saved with self.save_project
        """
        if askyesno("Attention","Toute progression non sauvegardée sera perdue. Continuer ?"):
            json_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            with open(json_path, 'r') as f:
                dict = json.load(f)
            
            self.toolbar.project_path = json_path
            self.origin_path = dict["origin_path"]
            self.load_set(path=self.origin_path)
            self.workspace.points = format_points(dict["img_dict"]["p1"])
            self.workspace.name_list = dict["img_dict"]["img_name"]
            self.workspace.max_points = len(self.workspace.points[0])
            self.workspace.draw_image()


    def export_project(self):
        """
        Exports (as a .dat file) the computed images.
        """
        pass