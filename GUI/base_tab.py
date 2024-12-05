import tkinter as tk
from tkinter import ttk


class BaseTab:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.frame = ttk.Frame(self.parent)
        self.trees = {}
        self.selected_dungeon_view = tk.StringVar()
        self.last_dungeon = tk.StringVar()

        self.table_container = ttk.Frame(self.frame)
        self.table_container.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.table_dropdown = ttk.Combobox(self.frame, textvariable=self.selected_dungeon_view)
        self.add_button = None
        self.subtract_button = None
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def create_new_table(self, dungeon):
        tree = ttk.Treeview(self.table_container, columns=("Item Name", "Value", "Quantity"), show='headings')
        tree.heading("Item Name", text="Item Name")
        tree.heading("Value", text="Value")
        tree.heading("Quantity", text="Quantity")
        self.trees[dungeon] = tree
        tree.grid(row=0, column=0, sticky="nsew")
        self.update_table_dropdown()

    def update_table_dropdown(self):
        self.table_dropdown['values'] = list(self.trees.keys())
        if not self.selected_dungeon_view.get():
            self.selected_dungeon_view.set(self.table_dropdown['values'][0])

    def refresh_tree(self, dungeon):
        if dungeon in self.trees:
            tree = self.trees[dungeon]
            for row in tree.get_children():
                tree.delete(row)

    def load_drops(self, dungeon):
        raise NotImplementedError("This method should be overridden by subclasses")

    def switch_table_view(self, event=None):
        dungeon = self.last_dungeon.get()
        if dungeon in self.trees:
            for d, tree in self.trees.items():
                tree.grid_remove()
            self.trees[dungeon].grid()
            self.load_drops(dungeon)
