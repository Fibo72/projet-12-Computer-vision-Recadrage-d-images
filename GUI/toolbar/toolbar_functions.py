from GUI.toolbar.drop_menu import DropMenu

def initiate(main_name, names, functions, master):
    drop_menu = DropMenu(main_name, master, names, functions)
    drop_menu.button.pack(side="left", padx=(1,0))
    return drop_menu