import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_DB = os.path.join(DATA_DIR, "users.json")

# Create folder if not exists
os.makedirs(DATA_DIR, exist_ok=True)

# Create file if not exists
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

# Load users safely
def load_users():
    try:
        with open(USER_DB, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except:
        return {}

# Save users safely
def save_users(users):
    try:
        with open(USER_DB, "w") as f:
            json.dump(users, f, indent=4)
    except:
        pass

# Signup function
def signup(name, email, phone, password):
    users = load_users()  # always returns dict

    if email in users:
        return False, "User already exists"

    users[email] = {
        "name": name,
        "phone": phone,
        "password": password
    }

    save_users(users)
    return True, "Signup successful"

# Login function
def login(email, password):
    users = load_users()

    if email in users and users[email]["password"] == password:
        return True, users[email]

    return False, None
