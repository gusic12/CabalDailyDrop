import json
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='cabal_drops.db', drops_file='dgs_list_drop.json'):
        self.drops_data = None
        self.dungeons = None
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.load_drops_from_file(drops_file)

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                item_value REAL NOT NULL,
                quantity INTEGER NOT NULL,
                timestamp REAL,
                drop_date TEXT NOT NULL,
                dungeon TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def load_drops_from_file(self, drops_file):
        with open(drops_file, 'r') as file:
            self.drops_data = json.load(file)
        self.dungeons = list(self.drops_data.keys())

    def get_all_item_names(self, dungeon):
        fixed_items = list(self.drops_data[dungeon].get("fixed_prices", {}).keys())
        range_items = list(self.drops_data[dungeon].get("range_prices", {}).keys())
        return sorted(fixed_items + range_items)

    def get_items_for_dungeon(self, dungeon):
        return list(self.drops_data.get(dungeon, {}).keys())

    def get_item_value(self, dungeon, item_name):
        fixed_prices = self.drops_data.get(dungeon, {}).get("fixed_prices", {})
        range_prices = self.drops_data.get(dungeon, {}).get("range_prices", {})

        if item_name in fixed_prices:
            return fixed_prices[item_name]
        elif item_name in range_prices:
            return range_prices[item_name]
        return None

    def get_last_item_value(self, item_name, dungeon):
        self.cursor.execute('SELECT item_value FROM drops WHERE item_name = ? AND dungeon = ? ORDER BY drop_date DESC LIMIT 1',
                            (item_name, dungeon))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def add_item(self, item_name, item_value, quantity, dungeon):
        item_value = int(item_value)
        timestamp = datetime.now().timestamp()
        drop_date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('SELECT id, quantity FROM drops WHERE item_name = ? AND dungeon = ? AND drop_date = ?',
                            (item_name, dungeon, drop_date))
        result = self.cursor.fetchone()
        if result:
            drop_id, current_quantity = result
            new_quantity = current_quantity + quantity
            self.cursor.execute('UPDATE drops SET quantity = ?, item_value = ?, timestamp = ? WHERE id = ?',
                                (new_quantity, item_value, timestamp, drop_id))
        else:
            self.cursor.execute(
                'INSERT INTO drops (item_name, item_value, quantity, drop_date, dungeon, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                (item_name, item_value, quantity, drop_date, dungeon, timestamp))
        self.conn.commit()

    def subtract_item(self, item_name, quantity, dungeon):
        drop_date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute(
            'SELECT id, quantity FROM drops WHERE item_name = ? AND dungeon = ? AND date(drop_date) = ?',
            (item_name, dungeon, drop_date))
        result = self.cursor.fetchone()
        if result:
            drop_id, current_quantity = result
            new_quantity = current_quantity - quantity
            if new_quantity > 0:
                self.cursor.execute('UPDATE drops SET quantity = ? WHERE id = ?', (new_quantity, drop_id))
            else:
                self.cursor.execute('DELETE FROM drops WHERE id = ?', (drop_id,))
            self.conn.commit()

    def get_drops_by_dungeon_and_date(self, dungeon, date):
        self.cursor.execute('SELECT item_name, item_value, quantity FROM drops WHERE dungeon = ? AND date(drop_date) = ?',
                            (dungeon, date))
        return self.cursor.fetchall()

    def get_all_dungeons(self):
        return self.dungeons

    def get_dates_by_dungeon(self, dungeon):
        self.cursor.execute('SELECT DISTINCT date(drop_date) FROM drops WHERE dungeon = ?', (dungeon,))
        return [row[0] for row in self.cursor.fetchall()]

    def clear_database(self):
        self.cursor.execute('DELETE FROM drops')
        self.conn.commit()

    def remove_item(self, item_name, dungeon):
        self.cursor.execute("DELETE FROM drops WHERE item_name = ? AND dungeon = ?", (item_name, dungeon))
        self.conn.commit()

    def close(self):
        self.conn.close()
