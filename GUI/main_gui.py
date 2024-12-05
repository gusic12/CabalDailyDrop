import tkinter as tk
from tkinter import ttk, messagebox

from DataBase.base import Database
from GUI.daily_drop import DayDropTab
from GUI.dungeon_drop import DungeonDropTab


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cabal Online Drop Tracker")

        self.db = Database()

        self.create_widgets()

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Clean Data Base", command=self.clear_database)

        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.day_tab = DayDropTab(self.tabControl, self.db)
        self.dungeon_tab = DungeonDropTab(self.tabControl, self.db)

        self.tabControl.add(self.day_tab.frame, text='Dzienny Drop')
        self.tabControl.add(self.dungeon_tab.frame, text='Dungeon Drop')

    def clear_database(self):
        self.db.clear_database()
        messagebox.showinfo("Informacja", "Baza danych została wyczyszczona.")
        self.day_tab.refresh_tree()
        self.dungeon_tab.refresh_tree()

    def run(self):
        self.root.mainloop()
