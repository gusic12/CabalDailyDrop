from datetime import datetime, timedelta

import tkinter as tk
from tkinter import ttk

from GUI.base_tab import BaseTab
from Helpers.helpers import convert_value, format_value


class DayDropTab(BaseTab):
    def __init__(self, parent, db):
        self.items = None
        self.dungeons = None
        self.dungeon_dropdown = None
        self.entry_item_name = None
        self.entry_item_value = None
        self.entry_quantity = None
        self.plus_button = None
        self.minus_button = None
        super().__init__(parent, db)

    def create_widgets(self):
        self.initialize_variables()
        self.create_styles()
        self.create_dungeon_widgets()
        self.create_form_widgets()
        self.create_table_view()
        self.configure_grid()
        self.switch_table_view()
        self.update_item_value()

    # ==============================================================================================================
    # ==============================    INITIALIZATION AND CONFIGURATION   =========================================
    # ==============================================================================================================

    def initialize_variables(self):
        self.dungeons = list(self.db.drops_data.keys())
        if self.dungeons:
            self.items = self.db.get_all_item_names(self.dungeons[0])
            self.last_dungeon.set(self.dungeons[0])

    @staticmethod
    def create_styles():
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 12), padding=5)
        style.configure('TButton', font=('Helvetica', 12), padding=5)
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))
        style.map('TButton', background=[('active', 'lightblue')])
        style.map('TCombobox', fieldbackground=[('active', 'lightblue')])

    # ==============================================================================================================
    # ======================================    DUNGEON WIDGETS    ================================================
    # ==============================================================================================================

    def create_dungeon_widgets(self):
        dungeon_frame = ttk.LabelFrame(self.frame, text="Select Dungeon", padding=(10, 10))
        dungeon_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(dungeon_frame, text="Dungeon:").grid(row=0, column=0, padx=5, pady=5)
        self.dungeon_dropdown = ttk.Combobox(dungeon_frame, textvariable=self.last_dungeon, style='TCombobox',
                                             state='readonly')
        self.dungeon_dropdown['values'] = self.dungeons
        self.dungeon_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.dungeon_dropdown.bind("<<ComboboxSelected>>", self.switch_table_view)

    # ==============================================================================================================
    # ======================================    FORM WIDGETS      ================================================
    # ==============================================================================================================

    def create_form_widgets(self):
        form_frame = ttk.LabelFrame(self.frame, text="Add Item", padding=(10, 10))
        form_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(form_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_item_name = ttk.Combobox(form_frame, style='TCombobox', state='readonly')
        self.entry_item_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_item_name.bind("<<ComboboxSelected>>", lambda _: self.update_item_value())

        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantity = ttk.Entry(form_frame, style='TEntry')
        self.entry_quantity.insert(0, "1")
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(form_frame, text="Item Value:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_item_value = ttk.Entry(form_frame, style='TEntry')
        self.entry_item_value.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text="Add Item", command=self.add_item, style='TButton').grid(row=3, column=0,
                                                                                             columnspan=2, pady=10)

    # ==============================================================================================================
    # =======================================   TABLE VIEW      ====================================================
    # ==============================================================================================================

    def create_table_view(self):
        table_container = ttk.Frame(self.frame)
        table_container.grid(row=2, column=0, sticky='nsew')
        self.table_container = table_container
        self.create_initial_tables()
        self.update_item_dropdown()

        if self.dungeons:
            self.last_dungeon.set(self.dungeons[0])
        if self.items:
            self.entry_item_name.set(self.items[0])

    def create_new_table(self, dungeon):
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
        style.configure('Treeview', font=('Helvetica', 12))

        tree = ttk.Treeview(self.table_container, columns=("Item Name", "Value", "Quantity"), show='headings',
                            selectmode='none', style='Treeview')

        tree.heading("Item Name", text="Item Name", anchor=tk.CENTER)
        tree.heading("Value", text="Value", anchor=tk.CENTER)
        tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)

        tree.column("Item Name", anchor=tk.CENTER)
        tree.column("Value", anchor=tk.CENTER)
        tree.column("Quantity", anchor=tk.CENTER)

        tree.bind("<Motion>", self.on_tree_enter)
        tree.bind("<Leave>", self.on_tree_leave)

        self.trees[dungeon] = tree
        self.update_table_dropdown()

        scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.table_container.grid_rowconfigure(0, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

    # ==============================================================================================================
    # ========================================   GRID CONFIGURATION   ==============================================
    # ==============================================================================================================

    def configure_grid(self):
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def update_item_value(self):
        item_name = self.entry_item_name.get()
        dungeon = self.last_dungeon.get()
        self.entry_item_value.config(state=tk.NORMAL)
        self.entry_item_value.delete(0, tk.END)

        if item_name:
            item_data = self.db.get_item_value(dungeon, item_name)

            if item_data:
                if isinstance(item_data, dict):
                    min_value = item_data["min_value"]
                    max_value = item_data["max_value"]
                    last_value = self.db.get_last_item_value(item_name, dungeon)

                    if last_value > 0:
                        self.entry_item_value.insert(0, format_value(last_value))
                    else:
                        self.entry_item_value.insert(0, format_value(min_value))

                    self.entry_item_value.config(state=tk.NORMAL)
                    self.entry_item_value.bind("<FocusOut>", lambda e: self.check_range_value(min_value, max_value))
                    self.entry_item_value.bind("<Enter>", lambda e: self.show_tooltip(e, min_value, max_value))
                    self.entry_item_value.bind("<Leave>", self.hide_tooltip)
                else:
                    self.entry_item_value.insert(0, format_value(item_data))
                    self.entry_item_value.config(state='readonly')

    def check_range_value(self, min_value, max_value):
        try:
            value = convert_value(self.entry_item_value.get())
            if value < min_value or value > max_value:
                self.entry_item_value.delete(0, tk.END)
                self.entry_item_value.insert(0, format_value(min_value))
        except ValueError:
            self.entry_item_value.delete(0, tk.END)
            self.entry_item_value.insert(0, format_value(min_value))

    def show_tooltip(self, event, min_value, max_value):
        tooltip_text = f"Allowed range: {min_value} - {max_value}"
        x = event.widget.winfo_rootx() + event.widget.winfo_width()
        y = event.widget.winfo_rooty() + event.widget.winfo_height()
        self.tooltip = tk.Toplevel(self.frame)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=tooltip_text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            delattr(self, 'tooltip')

    def update_item_dropdown(self, event=None):
        dungeon = self.last_dungeon.get()
        print("Selected dungeon:", dungeon)
        items = self.db.get_all_item_names(dungeon)
        print("Items for selected dungeon:", items)
        self.entry_item_name['values'] = items
        self.entry_item_value.config(state=tk.NORMAL)
        self.entry_item_value.delete(0, tk.END)
        self.entry_item_value.insert(0, "0")

    def add_item(self):
        item_name = self.entry_item_name.get()
        dungeon = self.last_dungeon.get()
        item_value = self.db.get_item_value(dungeon, item_name)
        if isinstance(item_value, dict):
            item_value = convert_value(self.entry_item_value.get())
        else:
            item_value = convert_value(self.entry_item_value.get())

        quantity = int(self.entry_quantity.get())

        self.db.add_item(item_name, item_value, quantity, dungeon)
        self.load_drops(dungeon)

    def create_initial_tables(self):
        for i, dungeon in enumerate(self.db.get_all_dungeons()):
            if dungeon not in self.trees:
                self.create_new_table(dungeon)
            for row in self.db.cursor.execute(
                    'SELECT item_name, item_value, quantity FROM drops WHERE dungeon = ? AND strftime("%s", "now") - strftime("%s", drop_date) <= 86400',
                    (dungeon,)):
                item_name, item_value, quantity = row
                item_value = int(item_value)
                self.trees[dungeon].insert("", "end", values=(item_name, item_value, quantity))
            if i == 0:
                self.last_dungeon.set(dungeon)
                self.switch_table_view()

    def load_drops(self, dungeon):
        tree = self.trees[dungeon]
        for row in tree.get_children():
            tree.delete(row)
        now = datetime.now()
        utc_plus_2 = now + timedelta(hours=2)
        today_22 = (utc_plus_2.replace(hour=22, minute=0, second=0, microsecond=0)).timestamp()
        yesterday_22 = (utc_plus_2.replace(hour=22, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp()
        current_time = utc_plus_2.timestamp()

        query = 'SELECT item_name, item_value, quantity FROM drops WHERE dungeon = ? AND timestamp BETWEEN ? AND ?'
        params = (dungeon, yesterday_22, today_22)
        self.db.cursor.execute(query, params)
        results = self.db.cursor.fetchall()

        for item_name, item_value, quantity in results:
            item_value = int(item_value)
            tree.insert("", "end", values=(item_name, item_value, quantity))

        if current_time >= today_22:
            for row in tree.get_children():
                tree.delete(row)

    def on_tree_enter(self, event):
        tree = event.widget
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        if item and column == '#3':
            if not self.plus_button:
                self.plus_button = tk.Button(tree, text="+", command=lambda: self.increment_quantity(tree, item))
            if not self.minus_button:
                self.minus_button = tk.Button(tree, text="-", command=lambda: self.decrement_quantity(tree, item))

            self.plus_button.config(command=lambda: self.increment_quantity(tree, item))
            self.minus_button.config(command=lambda: self.decrement_quantity(tree, item))

            bbox = tree.bbox(item, column)
            if bbox:
                self.plus_button.place(x=bbox[0] + bbox[2] - 20, y=bbox[1] + bbox[3] // 2, anchor=tk.CENTER)
                self.minus_button.place(x=bbox[0] + 20, y=bbox[1] + bbox[3] // 2, anchor=tk.CENTER)

    def on_tree_leave(self, event):
        if self.add_button:
            self.add_button.place_forget()
        if self.subtract_button:
            self.subtract_button.place_forget()

    def increment_quantity(self, tree, item):
        try:
            item_data = tree.item(item, "values")
            item_name, item_value, quantity = item_data
            quantity = int(quantity)
            self.db.add_item(item_name, float(item_value), 1, self.last_dungeon.get())
            tree.item(item, values=(item_name, item_value, str(quantity + 1)))
        except tk.TclError:
            pass

    def decrement_quantity(self, tree, item):
        try:
            item_data = tree.item(item, "values")
            item_name, item_value, quantity = item_data
            quantity = int(quantity)
            if quantity > 1:
                self.db.subtract_item(item_name, 1, self.last_dungeon.get())
                tree.item(item, values=(item_name, item_value, str(quantity - 1)))
            else:
                self.db.remove_item(item_name, self.last_dungeon.get())
                tree.delete(item)
        except tk.TclError:
            pass
