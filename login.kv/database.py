import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.db_name = 'farmers.db'
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name, timeout=10)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        try:
            # Create users table
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            # Create crops table
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS crops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                crop_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')

            # Create market_prices table
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS market_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_name TEXT UNIQUE NOT NULL,
                price TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    def add_user(self, username, password):
        try:
            self.cur.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        self.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (username, password))
        return self.cur.fetchone() is not None

    def get_user_id(self, username):
        self.cur.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def add_crop(self, user_id, crop_type, quantity, location):
        self.cur.execute('''
        INSERT INTO crops (user_id, crop_type, quantity, location)
        VALUES (?, ?, ?, ?)
        ''', (user_id, crop_type, quantity, location))
        self.conn.commit()

    def get_crops_by_user(self, user_id):
        self.cur.execute('''
        SELECT crop_type, quantity, location FROM crops
        WHERE user_id = ?
        ORDER BY created_at DESC
        ''', (user_id,))
        return self.cur.fetchall()

    def update_market_price(self, crop_name, price):
        try:
            # Close and reopen connection to avoid locked database
            self.conn.close()
            self.connect()
            
            self.cur.execute('''
            INSERT OR REPLACE INTO market_prices (crop_name, price, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (crop_name, str(price)))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating market price: {e}")
            self.conn.rollback()
            return False

    def get_market_prices(self):
        try:
            self.cur.execute('SELECT crop_name, price FROM market_prices')
            return dict(self.cur.fetchall())
        except sqlite3.Error as e:
            print(f"Error getting market prices: {e}")
            return {}

    def get_all_users(self):
        self.cur.execute('SELECT username FROM users')
        return [row[0] for row in self.cur.fetchall()]

    def get_user_crops_count(self, user_id):
        self.cur.execute('SELECT COUNT(*) FROM crops WHERE user_id = ?', (user_id,))
        return self.cur.fetchone()[0]

    def delete_crop(self, crop_id, user_id):
        self.cur.execute('DELETE FROM crops WHERE id = ? AND user_id = ?', 
                         (crop_id, user_id))
        self.conn.commit()
        return self.cur.rowcount > 0

    def update_crop(self, crop_id, user_id, quantity, location):
        self.cur.execute('''
        UPDATE crops 
        SET quantity = ?, location = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
        ''', (quantity, location, crop_id, user_id))
        self.conn.commit()
        return self.cur.rowcount > 0

    def delete_market_price(self, crop_name):
        try:
            self.cur.execute('DELETE FROM market_prices WHERE crop_name = ?', (crop_name,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting market price: {e}")
            self.conn.rollback()
            return False

    def delete_all_market_prices(self):
        try:
            self.cur.execute('DELETE FROM market_prices')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting all market prices: {e}")
            self.conn.rollback()
            return False

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass 