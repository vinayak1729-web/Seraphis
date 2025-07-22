import bcrypt
import json
import os
from datetime import datetime
from flask import current_app
from pymongo.errors import DuplicateKeyError
import logging

# JSON storage directory
JSON_DIR = "instance/user_data_json"
os.makedirs(JSON_DIR, exist_ok=True)

def load_users():
    users = []
    users_file = os.path.join(JSON_DIR, "users.json")
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    try:
        return users or list(current_app.mongo_db.users.find())  # Fallback to MongoDB
    except Exception:
        return users  # Return JSON data if MongoDB fails

def register_user(name, email, password):
    users_file = os.path.join(JSON_DIR, "users.json")
    users = load_users()

    if any(user['email'] == email or user['name'] == name for user in users):
        raise ValueError('Email or username already exists.')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'role': 'user',
        'created_at': datetime.now().isoformat(),
        'updated_at': None,
        'updated_by': None,
        'fhir_id': None
    }

    users.append(new_user)
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

    try:
        current_app.mongo_db.users.insert_one(new_user)
    except DuplicateKeyError:
        pass  # JSON already updated, Mongo sync handled separately

    return new_user

def login_user(identifier, password):
    users = load_users()
    user = next((u for u in users if u['email'] == identifier or u['name'] == identifier), None)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user
    return None

def log_activity(user_id, activity):
    activity_file = os.path.join(JSON_DIR, f"{user_id}_activities.json")
    activities = []
    if os.path.exists(activity_file):
        with open(activity_file, 'r') as f:
            activities = json.load(f)
    activities.append({'activity': activity, 'timestamp': datetime.now().isoformat()})
    with open(activity_file, 'w') as f:
        json.dump(activities, f, indent=4)