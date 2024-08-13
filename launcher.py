import os
import shutil
import subprocess
import json
from tkinter import Tk, filedialog, Button, Listbox, END

CIV_V_DLC_PATH = r"E:\SteamLibrary\steamapps\common\Sid Meier's Civilization V\Assets\DLC"
CIV_V_EXE_PATH = r"E:\SteamLibrary\steamapps\common\Sid Meier's Civilization V\CivilizationV.exe"
INSTALLED_MODS_FILE = "installed_mods.json"

class ModLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Civ V Mod Launcher")

        self.mods_path = ""
        self.mods = []
        self.installed_mods = self.load_installed_mods()

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

    def load_installed_mods(self):
        if os.path.exists(INSTALLED_MODS_FILE):
            with open(INSTALLED_MODS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_installed_mods(self):
        with open(INSTALLED_MODS_FILE, 'w') as f:
            json.dump(self.installed_mods, f)

    def launch_game(self):
        selected_indices = self.mod_listbox.curselection()
        if not selected_indices:
            print("No mod selected")
            return

        selected_mod = self.mods[selected_indices[0]]
        src_path = os.path.join(self.mods_path, selected_mod)
        dest_path = os.path.join(CIV_V_DLC_PATH, selected_mod)

        # Remove previously installed mods
        for mod in self.installed_mods:
            mod_path = os.path.join(CIV_V_DLC_PATH, mod)
            if os.path.exists(mod_path):
                shutil.rmtree(mod_path)

        # Install the selected mod
        shutil.copytree(src_path, dest_path)

        # Update the list of installed mods
        self.installed_mods = [selected_mod]
        self.save_installed_mods()

        # Launch the game
        subprocess.Popen(CIV_V_EXE_PATH)

        # Close the launcher
        self.master.quit()

if __name__ == "__main__":
    root = Tk()
    launcher = ModLauncher(root)
    root.mainloop()