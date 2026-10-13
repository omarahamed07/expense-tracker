import sqlite3
import datetime

DB_NAME = "expense.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    note TEXT,
    date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    
def add_expense(amount, category, note=None):
    date = datetime.date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
        (amount, category, note, date),
    )
    conn.commit()
    conn.close()