from datetime import datetime
from flask import current_app

def save_user_data(email, user_data):
    username = current_app.mongo_db.users.find_one({'email': email})['name']
    user_data['username'] = username
    user_data['timestamp'] = datetime.now().isoformat()
    current_app.mongo_db.user_data.update_one(
        {'username': username},
        {'$set': user_data},
        upsert=True
    )

def get_user_data(username):
    return current_app.mongo_db.user_data.find_one({'username': username})

def save_questionnaire_responses(username, response_type, responses):
    questionnaire_responses_col = current_app.mongo_db.questionnaire_responses
    response_doc = {
        'username': username,
        'type': response_type,
        'responses': responses,
        'timestamp': datetime.now().isoformat()
    }
    questionnaire_responses_col.insert_one(response_doc)

def get_questionnaire_responses(username):
    return list(current_app.mongo_db.questionnaire_responses.find({'username': username}))

def save_meditation_log(username, meditation_data):
    meditation_col = current_app.mongo_db.meditation_data
    meditation_doc = {
        'username': username,
        'timestamp': datetime.now().isoformat(),
        'duration': meditation_data.get('duration', 300),
        'completed': meditation_data.get('completed', True)
    }
    meditation_col.insert_one(meditation_doc)

def get_meditation_stats(username):
    meditation_col = current_app.mongo_db.meditation_data
    meditation_history = list(meditation_col.find({'username': username}))
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
    moods_col = current_app.mongo_db.mood_data
    mood_doc = {
        'username': username,
        'mood': mood_data['mood'],
        'timestamp': mood_data['timestamp']
    }
    moods_col.insert_one(mood_doc)

def get_moods(username):
    moods_col = current_app.mongo_db.mood_data
    moods = list(moods_col.find({'username': username}))
    moods.sort(key=lambda x: x['timestamp'])
    return moods