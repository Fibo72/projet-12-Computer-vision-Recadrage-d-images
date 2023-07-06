from GUI.toolbar.option_menus.points_menu import PointsMenu
from GUI.toolbar.option_menus.recadrage_menu import RecadrageMenu
from GUI.toolbar.option_menus.profile_menu import ProfileViewer

class MenusHandler():
    def __init__(self, master, toolbar) -> None:
        self.master = master
        self.toolbar = toolbar

    def createPointsMenu(self):
        PointsMenu(self.master, self.toolbar)
    
    def createRecadrageMenu(self):
        RecadrageMenu(self.master, self.toolbar)
    
    def createProfileMenu(self):
        ProfileViewer(self.master, self.toolbar)
    