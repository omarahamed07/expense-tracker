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
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id
def list_expenses(category=None, month=None):
    query = "SELECT id, amount, category, note, date FROM expenses"
    conditions = []
    params = []
    if category:
        conditions.append("category = ?")
        params.append(category)
    if month:
        conditions.append("substr(date, 1, 7) = ?")
        params.append(month)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY date DESC, id DESC"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_summary(month=None):
    query = "SELECT category, SUM(amount) FROM expenses"
    params = []
    if month:
        query += " WHERE substr(date, 1, 7) = ?"
        params.append(month)
    query += " GROUP BY category ORDER BY SUM(amount) DESC"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    total = sum(amount for _, amount in rows)
    return total, rows