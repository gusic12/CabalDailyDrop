from abc import ABC
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from GUI.base_tab import BaseTab


class DungeonDropTab(BaseTab, ABC):
    def __init__(self, parent, db):
        self.selected_dungeon = tk.StringVar()
        self.selected_date_from = tk.StringVar()
        self.selected_date_to = tk.StringVar()
        super().__init__(parent, db)

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self.frame, text="Wybór Dungeona", padding=(10, 10))
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Dungeon:").grid(row=0, column=0, padx=5, pady=5)
        self.dungeon_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_dungeon,
                                             values=self.db.get_all_dungeons())
        self.dungeon_dropdown.grid(row=0, column=1, padx=5, pady=5)

        date_frame = ttk.LabelFrame(self.frame, text="Zakres Dat", padding=(10, 10))
        date_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(date_frame, text="Od:").grid(row=0, column=0)
        self.date_from_entry = DateEntry(date_frame, textvariable=self.selected_date_from, date_pattern='yyyy-mm-dd')
        self.date_from_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(date_frame, text="Do:").grid(row=1, column=0)
        self.date_to_entry = DateEntry(date_frame, textvariable=self.selected_date_to, date_pattern='yyyy-mm-dd')
        self.date_to_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(date_frame, text="Pokaż Drop", command=self.show_dungeon_drops).grid(row=2, column=0, columnspan=2,
                                                                                        pady=10)

    def show_dungeon_drops(self):
        dungeon = self.selected_dungeon.get()
        date_from = self.selected_date_from.get()
        date_to = self.selected_date_to.get()
        self.refresh_dungeon_tree(dungeon, date_from, date_to)

    def refresh_dungeon_tree(self, dungeon, date_from, date_to):
        if dungeon in self.trees:
            tree = self.trees[dungeon]
            for row in tree.get_children():
                tree.delete(row)
            self.load_dungeon_drops(dungeon, date_from, date_to)
        else:
            self.create_new_table(dungeon)
            self.load_dungeon_drops(dungeon, date_from, date_to)

    def load_dungeon_drops(self, dungeon, date_from, date_to):
        query = '''
            SELECT item_name, item_value, quantity 
            FROM drops 
            WHERE dungeon = ? AND drop_date BETWEEN ? AND ?
        '''
        self.db.cursor.execute(query, (dungeon, date_from, date_to))
        results = self.db.cursor.fetchall()
        for item_name, item_value, quantity in results:
            item_value = int(item_value)
            self.trees[dungeon].insert("", "end", values=(item_name, item_value, quantity))
