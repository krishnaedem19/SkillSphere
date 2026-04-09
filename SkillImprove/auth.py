import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# Create DB and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT,
        phone TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Signup
def signup(name, email, phone, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                  (email, name, phone, password))
        conn.commit()
        return True, "Signup successful"
    except:
        return False, "User already exists"
    finally:
        conn.close()

# Login
def login(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name, phone FROM users WHERE email=? AND password=?",
              (email, password))

    user = c.fetchone()
    conn.close()

    if user:
        return True, {"name": user[0], "phone": user[1]}
    return False, None
