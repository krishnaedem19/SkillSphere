import json
import os
import re

USER_DB = "data/users.json"

def load_users():
    if not os.path.exists(USER_DB):
        return []
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^[6-9]\d{9}$", phone)

def signup(name, email, phone, password):
    users = load_users()

    if not is_valid_email(email):
        return False, "Invalid email"

    if not is_valid_phone(phone):
        return False, "Invalid phone"

    for user in users:
        if user["email"] == email or user["phone"] == phone:
            return False, "User already exists"

    users.append({
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    })

    save_users(users)
    return True, "Signup successful"

def login(email, password):
    users = load_users()

    for user in users:
        if user["email"] == email and user["password"] == password:
            return True, user

    return False, "Invalid credentials"