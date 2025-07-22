import json
import os
import csv
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client[os.getenv("MONGO_DB_NAME", "Seraphis_db")]

# Clear existing collections
db.users.drop()
db.user_data.drop()
db.appointments.drop()
db.appointment_stats.drop()
db.doctor_appointments.drop()
db.questionnaire_responses.drop()
db.meditation_data.drop()
db.mood_data.drop()
db.ratings.drop()

# JSON storage directory
JSON_DIR = "instance/user_data_json"

# Migrate users.json
users_file = os.path.join(JSON_DIR, "users.json")
if os.path.exists(users_file):
    with open(users_file, "r") as file:
        users = json.load(file)
        for user in users:
            db.users.insert_one(user)

# Migrate user_data
for filename in os.listdir(JSON_DIR):
    if filename.endswith("_user_data.json"):
        username = filename[:-12]
        with open(os.path.join(JSON_DIR, filename), "r") as file:
            user_data = json.load(file)
            db.user_data.insert_one(user_data)

# Migrate appointments
for filename in os.listdir("instance/appointments"):
    if filename.endswith(".json"):
        username = filename[:-5]
        with open(f"instance/appointments/{filename}", "r") as file:
            appointments = json.load(file)
            for appointment in appointments:
                appointment["patient"] = username
                db.appointments.insert_one(appointment)

# Migrate appointment_stats
for filename in os.listdir("instance/appointment_stats"):
    if filename.endswith(".json"):
        username = filename[:-5]
        with open(f"instance/appointment_stats/{filename}", "r") as file:
            stats = json.load(file)
            stats["username"] = username
            db.appointment_stats.insert_one(stats)

# Migrate doctor_appointments
for filename in os.listdir("instance/doctor_appointments"):
    if filename.endswith(".json"):
        with open(f"instance/doctor_appointments/{filename}", "r") as file:
            doctor_appointments = json.load(file)
            for appointment in doctor_appointments:
                db.doctor_appointments.insert_one(appointment)

# Migrate questionnaire responses
for folder in ['closed_ended', 'open_ended']:
    folder_path = os.path.join(JSON_DIR, folder)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                username = filename.split('_')[0]
                with open(os.path.join(folder_path, filename), "r") as file:
                    responses = json.load(file)
                    db.questionnaire_responses.insert_one(responses)

# Migrate meditation_data
for filename in os.listdir(JSON_DIR):
    if filename.endswith("_meditation_log.json"):
        username = filename.split('_')[0]
        with open(os.path.join(JSON_DIR, filename), "r") as file:
            meditation_history = json.load(file)
            for session in meditation_history:
                db.meditation_data.insert_one(session)

# Migrate mood_data
for filename in os.listdir(JSON_DIR):
    if filename.endswith("_moods.json"):
        username = filename.split('_')[0]
        with open(os.path.join(JSON_DIR, filename), "r") as file:
            moods = json.load(file)
            for mood in moods:
                db.mood_data.insert_one(mood)

# Migrate ratings
ratings_file = "instance/rating/ratings.json"
if os.path.exists(ratings_file):
    with open(ratings_file, "r") as file:
        ratings_data = json.load(file)
        for rating in ratings_data["ratings"]:
            db.ratings.insert_one(rating)

print("Migration completed successfully at 11:35 AM IST, July 18, 2025!")