import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="budget.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_transaction(self, type_, amount, category):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO transactions (type, amount, category, date)
            VALUES (?, ?, ?, ?)
        ''', (type_, amount, category, date))
        self.conn.commit()

    def get_monthly_summary(self, month, year):
        self.cursor.execute('''
            SELECT type, SUM(amount) as total
            FROM transactions
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY type
        ''', (f"{month:02d}", str(year)))
        return self.cursor.fetchall()

    def get_category_summary(self, month, year):
        self.cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
        ''', (f"{month:02d}", str(year)))
        return self.cursor.fetchall()

    def get_all_transactions(self):
        self.cursor.execute('''
            SELECT id, type, amount, category, date
            FROM transactions
            ORDER BY date DESC
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close() 