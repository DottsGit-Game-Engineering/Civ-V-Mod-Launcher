import os
import shutil
import subprocess
from tkinter import Tk, filedialog, Button, Listbox, END

# Constants
CIV_V_DLC_PATH = r"E:\SteamLibrary\steamapps\common\Sid Meier's Civilization V\Assets\DLC"
CIV_V_EXE_PATH = r"E:\SteamLibrary\steamapps\common\Sid Meier's Civilization V\CivilizationV.exe"

class ModLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Civ V Mod Launcher")

        self.mods_path = ""
        self.mods = []

        # Create and pack widgets
        self.select_folder_button = Button(master, text="Select Mods Folder", command=self.select_mods_folder)
        self.select_folder_button.pack()

        self.mod_listbox = Listbox(master)
        self.mod_listbox.pack()

        self.launch_button = Button(master, text="Launch with Selected Mod", command=self.launch_game)
        self.launch_button.pack()

    def select_mods_folder(self):
        self.mods_path = filedialog.askdirectory()
        self.update_mod_list()

    def update_mod_list(self):
        self.mods = [f for f in os.listdir(self.mods_path) if os.path.isdir(os.path.join(self.mods_path, f))]
        self.mod_listbox.delete(0, END)
        for mod in self.mods:
            self.mod_listbox.insert(END, mod)

    def launch_game(self):
        selected_indices = self.mod_listbox.curselection()
        if not selected_indices:
            print("No mod selected")
            return

        selected_mod = self.mods[selected_indices[0]]
        src_path = os.path.join(self.mods_path, selected_mod)
        dest_path = os.path.join(CIV_V_DLC_PATH, selected_mod)

        # Move the mod folder
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(src_path, dest_path)

        # Launch the game
        subprocess.Popen(CIV_V_EXE_PATH)

        # Close the launcher
        self.master.quit()

if __name__ == "__main__":
    root = Tk()
    launcher = ModLauncher(root)
    root.mainloop()