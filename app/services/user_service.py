from datetime import datetime
from flask import current_app
import json
import os

# JSON storage directory
JSON_DIR = "instance/user_data_json"
os.makedirs(JSON_DIR, exist_ok=True)

def save_user_data(email, user_data):
    username = current_app.mongo_db.users.find_one({'email': email})['name']
    user_data['username'] = username
    user_data['timestamp'] = datetime.now().isoformat()
    user_file = os.path.join(JSON_DIR, f"{username}_user_data.json")
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=4)
    current_app.mongo_db.user_data.update_one(
        {'username': username},
        {'$set': user_data},
        upsert=True
    )
    return user_data

def get_user_data(username):
    user_file = os.path.join(JSON_DIR, f"{username}_user_data.json")
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    return current_app.mongo_db.user_data.find_one({'username': username})

def save_questionnaire_responses(username, response_type, responses):
    response_doc = {
        'username': username,
        'type': response_type,
        'responses': responses,
        'timestamp': datetime.now().isoformat()
    }
    response_file = os.path.join(JSON_DIR, f"{username}_{response_type}_responses.json")
    with open(response_file, 'w') as f:
        json.dump(response_doc, f, indent=4)
    current_app.mongo_db.questionnaire_responses.insert_one(response_doc)

def get_questionnaire_responses(username):
    responses = []
    for response_type in ['closed_ended', 'open_ended']:
        response_file = os.path.join(JSON_DIR, f"{username}_{response_type}_responses.json")
        if os.path.exists(response_file):
            with open(response_file, 'r') as f:
                responses.append(json.load(f))
    if not responses:
        return list(current_app.mongo_db.questionnaire_responses.find({'username': username}))
    return responses

def save_meditation_log(username, meditation_data):
    meditation_doc = {
        'username': username,
        'timestamp': datetime.now().isoformat(),
        'duration': meditation_data.get('duration', 300),
        'completed': meditation_data.get('completed', True)
    }
    meditation_file = os.path.join(JSON_DIR, f"{username}_meditation_log.json")
    meditations = []
    if os.path.exists(meditation_file):
        with open(meditation_file, 'r') as f:
            meditations = json.load(f)
    meditations.append(meditation_doc)
    with open(meditation_file, 'w') as f:
        json.dump(meditations, f, indent=4)
    current_app.mongo_db.meditation_data.insert_one(meditation_doc)

def get_meditation_stats(username):
    meditation_file = os.path.join(JSON_DIR, f"{username}_meditation_log.json")
    if os.path.exists(meditation_file):
        with open(meditation_file, 'r') as f:
            meditation_history = json.load(f)
    else:
        meditation_history = list(current_app.mongo_db.meditation_data.find({'username': username}))
    if not meditation_history:
        return {'total_minutes': 0, 'total_sessions': 0, 'recent_sessions': []}
    total_minutes = sum(session['duration'] for session in meditation_history)
    total_sessions = len(meditation_history)
    return {
        'total_minutes': total_minutes,
        'total_sessions': total_sessions,
        'recent_sessions': meditation_history[-5:]
    }

def save_mood(username, mood_data):
    mood_doc = {
        'username': username,
        'mood': mood_data['mood'],
        'timestamp': mood_data['timestamp']
    }
    mood_file = os.path.join(JSON_DIR, f"{username}_moods.json")
    moods = []
    if os.path.exists(mood_file):
        with open(mood_file, 'r') as f:
            moods = json.load(f)
    moods.append(mood_doc)
    with open(mood_file, 'w') as f:
        json.dump(moods, f, indent=4)
    current_app.mongo_db.mood_data.insert_one(mood_doc)

def get_moods(username):
    mood_file = os.path.join(JSON_DIR, f"{username}_moods.json")
    if os.path.exists(mood_file):
        with open(mood_file, 'r') as f:
            moods = json.load(f)
            moods.sort(key=lambda x: x['timestamp'])
            return moods
    moods = list(current_app.mongo_db.mood_data.find({'username': username}))
    moods.sort(key=lambda x: x['timestamp'])
    return moods