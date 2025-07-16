import bcrypt
from datetime import datetime
from flask import current_app
from pymongo.errors import DuplicateKeyError
import logging

def load_users():
    return list(current_app.mongo_db.users.find())

def register_user(name, email, password):
    users_col = current_app.mongo_db.users

    if users_col.find_one({'$or': [{'email': email}, {'name': name}]}):
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

    try:
        users_col.insert_one(new_user)
    except DuplicateKeyError:
        raise ValueError('Email or username already exists.')

    return new_user

def login_user(identifier, password):
    user = current_app.mongo_db.users.find_one({
        '$or': [{'email': identifier}, {'name': identifier}]
    })
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user
    return None