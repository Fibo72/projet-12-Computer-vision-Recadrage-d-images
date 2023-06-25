from Aymeric.decode_img import get_phase_img
from tkinter import filedialog
from PIL import Image, ImageTk
from GUI.settings import check_file_format, get_scale
import os

class SaveLoadHandler():
    def __init__(self, toolbar) -> None:
        self.toolbar = toolbar
        self.workspace = toolbar.workspace
        self.side_m = toolbar.side_m

    def load_set(self):
        """
        Loads a set of .dat images localized in a single folder
        """
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

    def save_project(self):
        """
        Saves a project in a JSON file among others, it will save
            - path of the images (the JSON is loded in the same folder)
            - points on each images
        """
        pass

    def load_project(self):
        """
        Loads a project previously saved with self.save_project
        """
        pass

    def export_project(self):
        """
        Exports (as a .dat file) the computed images.
        """
        pass