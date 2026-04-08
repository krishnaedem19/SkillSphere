import json
import os

# ---------- PATH SETUP ---------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_DB = os.path.join(DATA_DIR, "users.json")

# ---------- CREATE FOLDER ---------- #
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- CREATE FILE IF NOT EXISTS ---------- #
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

# ---------- LOAD USERS ---------- #
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return {}

# ---------- SAVE USERS ---------- #
def save_users(users):
    try:
        with open(USER_DB, "w") as f:
            json.dump(users, f, indent=4)
    except:
        pass  # prevents crash

# ---------- SIGNUP FUNCTION ---------- #
def signup(name, email, phone, password):
    users = load_users()

    if email in users:
        return False, "User already exists"

    users[email] = {
        "name": name,
        "phone": phone,
        "password": password
    }

    save_users(users)
    return True, "Signup successful"

# ---------- LOGIN FUNCTION ---------- #
def login(email, password):
    users = load_users()

    if email in users and users[email]["password"] == password:
        return True, users[email]

    return False, None
