from Aymeric.decode_img import recadrage
from tkinter.messagebox import showinfo

class Computer():
    def __init__(self, toolbar) -> None:
        self.toolbar = toolbar
    
    def compute(self):
        if self.toolbar.project_path == None :
            showinfo("Attention", "Veuillez enregistrer votre projet avant de lancer le calcul")
        else :
            path_to_json = self.toolbar.project_path
            recadrage(path_to_json)
        