# import streamlit as st
# import json
# import os
# import datetime
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import smtplib
# from email.mime.text import MIMEText
# import uuid
# import bcrypt
# import re

# # Google Calendar API setup
# SCOPES = ["https://www.googleapis.com/auth/calendar"]

# # File paths for JSON storage
# USERS_FILE = "db/users.json"
# APPOINTMENTS_FILE = "db/appointments.json"

# # Initialize JSON files if they don't exist
# def init_db():
#     if not os.path.exists("db"):
#         os.makedirs("db")
#     if not os.path.exists(USERS_FILE):
#         with open(USERS_FILE, "w") as f:
#             json.dump({"users": []}, f)
#     if not os.path.exists(APPOINTMENTS_FILE):
#         with open(APPOINTMENTS_FILE, "w") as f:
#             json.dump({"appointments": []}, f)

# # User management functions
# def load_users():
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)["users"]

# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump({"users": users}, f, indent=2)

# def load_appointments():
#     with open(APPOINTMENTS_FILE, "r") as f:
#         return json.load(f)["appointments"]

# def save_appointments(appointments):
#     with open(APPOINTMENTS_FILE, "w") as f:
#         json.dump({"appointments": appointments}, f, indent=2)

# def hash_password(password):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# def check_password(password, hashed):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# # Email validation
# def is_valid_email(email):
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None

# # Google Calendar integration
# def get_calendar_service():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     return build("calendar", "v3", credentials=creds)

# # Email sending function
# def send_email(to_email, subject, body):
#     try:
#         smtp_server = "smtp.gmail.com"
#         smtp_port = 587
#         sender_email = "suryaprabha.hackathon@gmail.com"  # Replace with your email
#         sender_password = "gakx zapx wagp nrsg"  # Replace with your app password
        
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = sender_email
#         msg['To'] = to_email

#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
#         return True
#     except Exception as e:
#         st.error(f"Failed to send email: {e}")
#         return False

# # Create Google Calendar event
# def create_calendar_event(service, start_time, end_time, summary, attendees):
#     event = {
#         'summary': summary,
#         'start': {
#             'dateTime': start_time.isoformat(),
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': end_time.isoformat(),
#             'timeZone': 'UTC',
#         },
#         'attendees': [{'email': email} for email in attendees],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 30},
#             ],
#         },
#     }
    
#     try:
#         event = service.events().insert(calendarId='primary', body=event).execute()
#         return event.get('htmlLink')
#     except HttpError as error:
#         st.error(f"An error occurred: {error}")
#         return None

# # Main Streamlit app
# def main():
#     init_db()
    
#     st.set_page_config(page_title="Doctor Appointment System", layout="wide")
    
#     if 'user' not in st.session_state:
#         st.session_state.user = None
    
#     # Sidebar navigation
#     st.sidebar.title("Navigation")
#     if st.session_state.user:
#         st.sidebar.write(f"Logged in as: {st.session_state.user['email']}")
#         page = st.sidebar.radio("Go to", ["Home", "Profile", "Logout"])
#     else:
#         page = st.sidebar.radio("Go to", ["Login", "Register"])
    
#     if page == "Logout":
#         st.session_state.user = None
#         st.rerun()
    
#     users = load_users()
#     appointments = load_appointments()
    
#     # Login page
#     if page == "Login":
#         st.title("Login")
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         role = st.selectbox("Role", ["user", "doctor", "admin"])
        
#         if st.button("Login"):
#             if not is_valid_email(email):
#                 st.error("Invalid email format")
#             else:
#                 user = next((u for u in users if u['email'] == email and u['role'] == role), None)
#                 if user and check_password(password, user['password']):
#                     st.session_state.user = user
#                     st.success("Logged in successfully!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid credentials or role")
    
#     # Register page
#     elif page == "Register":
#         st.title("Register")
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         name = st.text_input("Name")
        
#         if st.button("Register"):
#             if not is_valid_email(email):
#                 st.error("Invalid email format")
#             elif any(u['email'] == email for u in users):
#                 st.error("Email already registered")
#             elif len(password) < 6:
#                 st.error("Password must be at least 6 characters")
#             else:
#                 new_user = {
#                     'id': str(uuid.uuid4()),
#                     'email': email,
#                     'password': hash_password(password),
#                     'name': name,
#                     'role': 'user'
#                 }
#                 users.append(new_user)
#                 save_users(users)
#                 st.success("Registered successfully! Please login.")
    
#     # Home page based on role
#     elif page == "Home":
#         if st.session_state.user['role'] == 'admin':
#             st.title("Admin Dashboard")
#             st.subheader("Create Doctor")
#             doc_email = st.text_input("Doctor Email")
#             doc_name = st.text_input("Doctor Name")
#             doc_password = st.text_input("Doctor Password", type="password")
            
#             if st.button("Create Doctor"):
#                 if not is_valid_email(doc_email):
#                     st.error("Invalid email format")
#                 elif any(u['email'] == doc_email for u in users):
#                     st.error("Email already registered")
#                 else:
#                     new_doctor = {
#                         'id': str(uuid.uuid4()),
#                         'email': doc_email,
#                         'password': hash_password(doc_password),
#                         'name': doc_name,
#                         'role': 'doctor'
#                     }
#                     users.append(new_doctor)
#                     save_users(users)
#                     st.success("Doctor created successfully!")
            
#             st.subheader("All Users")
#             for user in users:
#                 st.write(f"ID: {user['id']}, Email: {user['email']}, Name: {user['name']}, Role: {user['role']}")
        
#         elif st.session_state.user['role'] == 'doctor':
#             st.title("Doctor Dashboard")
#             st.subheader("Pending Appointment Requests")
            
#             doctor_appointments = [a for a in appointments if a['doctor_id'] == st.session_state.user['id'] and a['status'] == 'pending']
            
#             for appointment in doctor_appointments:
#                 user = next(u for u in users if u['id'] == appointment['user_id'])
#                 col1, col2, col3 = st.columns(3)
                
#                 with col1:
#                     st.write(f"Patient: {user['name']}")
#                     st.write(f"Date: {appointment['date']}")
#                     st.write(f"Time: {appointment['time']}")
                
#                 with col2:
#                     if st.button("Accept", key=f"accept_{appointment['id']}"):
#                         appointment['status'] = 'accepted'
#                         save_appointments(appointments)
                        
#                         service = get_calendar_service()
#                         start_time = datetime.datetime.fromisoformat(f"{appointment['date']}T{appointment['time']}+00:00")
#                         end_time = start_time + datetime.timedelta(minutes=30)
                        
#                         calendar_link = create_calendar_event(
#                             service,
#                             start_time,
#                             end_time,
#                             f"Appointment with {user['name']}",
#                             [user['email'], st.session_state.user['email']]
#                         )
                        
#                         if calendar_link:
#                             # Send email to user and doctor
#                             body = f"""Dear {user['name']},
                            
# Your appointment with Dr. {st.session_state.user['name']} has been confirmed.
# Date: {appointment['date']}
# Time: {appointment['time']}
# Calendar Link: {calendar_link}

# Best regards,
# Appointment System"""
                            
#                             send_email(user['email'], "Appointment Confirmation", body)
#                             send_email(st.session_state.user['email'], "Appointment Confirmation", body)
#                             st.success("Appointment accepted and calendar invites sent!")
                
#                 with col3:
#                     if st.button("Reschedule", key=f"reschedule_{appointment['id']}"):
#                         new_date = st.text_input("New Date (YYYY-MM-DD)", key=f"date_{appointment['id']}")
#                         new_time = st.text_input("New Time (HH:MM)", key=f"time_{appointment['id']}")
#                         if st.button("Confirm Reschedule", key=f"confirm_reschedule_{appointment['id']}"):
#                             appointment['date'] = new_date
#                             appointment['time'] = new_time
#                             appointment['status'] = 'rescheduled'
#                             save_appointments(appointments)
                            
#                             body = f"""Dear {user['name']},
                            
# Your appointment with Dr. {st.session_state.user['name']} has been rescheduled.
# New Date: {new_date}
# New Time: {new_time}

# Please confirm the new schedule.

# Best regards,
# Appointment System"""
#                             send_email(user['email'], "Appointment Rescheduled", body)
#                             st.success("Appointment rescheduled!")
                    
#                     if st.button("Cancel", key=f"cancel_{appointment['id']}"):
#                         appointment['status'] = 'cancelled'
#                         save_appointments(appointments)
                        
#                         body = f"""Dear {user['name']},
                        
# Your appointment with Dr. {st.session_state.user['name']} has been cancelled.

# Best regards,
# Appointment System"""
#                         send_email(user['email'], "Appointment Cancelled", body)
#                         st.success("Appointment cancelled!")
        
#         elif st.session_state.user['role'] == 'user':
#             st.title("User Dashboard")
#             st.subheader("Request Appointment")
            
#             doctors = [u for u in users if u['role'] == 'doctor']
#             doctor_names = [d['name'] for d in doctors]
#             selected_doctor = st.selectbox("Select Doctor", doctor_names)
#             date = st.text_input("Date (YYYY-MM-DD)")
#             time = st.text_input("Time (HH:MM)")
            
#             if st.button("Request Appointment"):
#                 try:
#                     datetime.datetime.strptime(date, '%Y-%m-%d')
#                     datetime.datetime.strptime(time, '%H:%M')
#                     doctor = next(d for d in doctors if d['name'] == selected_doctor)
                    
#                     new_appointment = {
#                         'id': str(uuid.uuid4()),
#                         'user_id': st.session_state.user['id'],
#                         'doctor_id': doctor['id'],
#                         'date': date,
#                         'time': time,
#                         'status': 'pending'
#                     }
#                     appointments.append(new_appointment)
#                     save_appointments(appointments)
                    
#                     body = f"""Dear Dr. {doctor['name']},
                    
# A new appointment request from {st.session_state.user['name']}:
# Date: {date}
# Time: {time}

# Please review and respond to this request.

# Best regards,
# Appointment System"""
#                     send_email(doctor['email'], "New Appointment Request", body)
#                     st.success("Appointment request sent!")
                    
#                 except ValueError:
#                     st.error("Invalid date or time format")
            
#             st.subheader("Your Appointments")
#             user_appointments = [a for a in appointments if a['user_id'] == st.session_state.user['id']]
#             for appointment in user_appointments:
#                 doctor = next(u for u in users if u['id'] == appointment['doctor_id'])
#                 st.write(f"Doctor: {doctor['name']}")
#                 st.write(f"Date: {appointment['date']}")
#                 st.write(f"Time: {appointment['time']}")
#                 st.write(f"Status: {appointment['status']}")
#                 st.write("---")

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import smtplib
from email.mime.text import MIMEText
import uuid
import bcrypt
import re

# Google Calendar API setup
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# File paths for JSON storage
USERS_FILE = "db/users.json"
APPOINTMENTS_FILE = "db/appointments.json"

# Initialize JSON files if they don't exist
def init_db():
    if not os.path.exists("db"):
        os.makedirs("db")
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"users": []}, f)
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "w") as f:
            json.dump({"appointments": []}, f)

# User management functions
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)["users"]

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)

def load_appointments():
    with open(APPOINTMENTS_FILE, "r") as f:
        return json.load(f)["appointments"]

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump({"appointments": appointments}, f, indent=2)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Google Calendar integration
def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

# Email sending function with styled HTML
def send_email(to_email, subject, body, sender_name, recipient_name):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "suryaprabha.hackathon@gmail.com"  # Replace with your email
        sender_password = "gakx zapx wagp nrsg"  # Replace with your app password
        
        # HTML email template with CSS styling
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    h2 {{ color: #2c3e50; }}
                    p {{ margin: 10px 0; }}
                    .highlight {{ color: #2980b9; font-weight: bold; }}
                    .footer {{ margin-top: 20px; font-size: 0.9em; color: #7f8c8d; text-align: center; }}
                    a {{ color: #3498db; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Appointment System Notification</h2>
                    <p>Dear {recipient_name},</p>
                    <p>{body}</p>
                    <p class="footer">Best regards,<br>{sender_name}<br>Appointment System</p>
                </div>
            </body>
        </html>
        """
        
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Create Google Calendar event
def create_calendar_event(service, start_time, end_time, summary, attendees):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink')
    except HttpError as error:
        st.error(f"An error occurred: {error}")
        return None

# Main Streamlit app
def main():
    init_db()
    
    # Add custom CSS for Streamlit interface
    st.markdown("""
        <style>
            .main { background-color: #f8f9fa; padding: 20px; border-radius: 10px; }
            .stButton>button { background-color: #3498db; color: white; border-radius: 5px; }
            .stButton>button:hover { background-color: #2980b9; }
            .stTextInput>div>input { border-radius: 5px; }
            .stSelectbox>div>select { border-radius: 5px; }
            h1, h2, h3 { color: #2c3e50; }
            .sidebar .sidebar-content { background-color: #ecf0f1; }
        </style>
    """, unsafe_allow_html=True)
    
    st.set_page_config(page_title="Doctor Appointment System", layout="wide")
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("### Welcome to the Appointment System")
    if st.session_state.user:
        st.sidebar.write(f"Logged in as: {st.session_state.user['email']}")
        page = st.sidebar.radio("Go to", ["Home", "Profile", "Logout"])
    else:
        page = st.sidebar.radio("Go to", ["Login", "Register"])
    
    if page == "Logout":
        st.session_state.user = None
        st.rerun()
    
    users = load_users()
    appointments = load_appointments()
    
    # Login page
    if page == "Login":
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "doctor", "admin"])
        
        if st.button("Login"):
            if not is_valid_email(email):
                st.error("Invalid email format")
            else:
                user = next((u for u in users if u['email'] == email and u['role'] == role), None)
                if user and check_password(password, user['password']):
                    st.session_state.user = user
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or role")
    
    # Register page
    elif page == "Register":
        st.title("Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name")
        
        if st.button("Register"):
            if not is_valid_email(email):
                st.error("Invalid email format")
            elif any(u['email'] == email for u in users):
                st.error("Email already registered")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                new_user = {
                    'id': str(uuid.uuid4()),
                    'email': email,
                    'password': hash_password(password),
                    'name': name,
                    'role': 'user'
                }
                users.append(new_user)
                save_users(users)
                st.success("Registered successfully! Please login.")
    
    # Home page based on role
    elif page == "Home":
        if st.session_state.user['role'] == 'admin':
            st.title("Admin Dashboard")
            st.subheader("Create Doctor")
            doc_email = st.text_input("Doctor Email")
            doc_name = st.text_input("Doctor Name")
            doc_password = st.text_input("Doctor Password", type="password")
            
            if st.button("Create Doctor"):
                if not is_valid_email(doc_email):
                    st.error("Invalid email format")
                elif any(u['email'] == doc_email for u in users):
                    st.error("Email already registered")
                else:
                    new_doctor = {
                        'id': str(uuid.uuid4()),
                        'email': doc_email,
                        'password': hash_password(doc_password),
                        'name': doc_name,
                        'role': 'doctor'
                    }
                    users.append(new_doctor)
                    save_users(users)
                    st.success("Doctor created successfully!")
            
            st.subheader("All Users")
            for user in users:
                st.write(f"ID: {user['id']}, Email: {user['email']}, Name: {user['name']}, Role: {user['role']}")
        
        elif st.session_state.user['role'] == 'doctor':
            st.title("Doctor Dashboard")
            st.subheader("Pending Appointment Requests")
            
            doctor_appointments = [a for a in appointments if a['doctor_id'] == st.session_state.user['id'] and a['status'] == 'pending']
            
            for appointment in doctor_appointments:
                user = next(u for u in users if u['id'] == appointment['user_id'])
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"Patient: {user['name']}")
                    st.write(f"Date: {appointment['date']}")
                    st.write(f"Time: {appointment['time']}")
                
                with col2:
                    if st.button("Accept", key=f"accept_{appointment['id']}"):
                        appointment['status'] = 'accepted'
                        save_appointments(appointments)
                        
                        service = get_calendar_service()
                        # Ensure time is in HH:MM format with leading zeros
                        time_parts = appointment['time'].split(':')
                        formatted_time = f"{int(time_parts[0]):02d}:{int(time_parts[1]):02d}"
                        start_time = datetime.datetime.fromisoformat(f"{appointment['date']}T{formatted_time}:00+00:00")
                        end_time = start_time + datetime.timedelta(minutes=30)
                        
                        calendar_link = create_calendar_event(
                            service,
                            start_time,
                            end_time,
                            f"Appointment with {user['name']}",
                            [user['email'], st.session_state.user['email']]
                        )
                        
                        if calendar_link:
                            # Send styled email to user and doctor
                            body = f"""Your appointment with Dr. {st.session_state.user['name']} has been confirmed.<br>
                            <span class="highlight">Date:</span> {appointment['date']}<br>
                            <span class="highlight">Time:</span> {appointment['time']}<br>
                            <a href="{calendar_link}">Add to Calendar</a>"""
                            
                            send_email(user['email'], "Appointment Confirmation", body, st.session_state.user['name'], user['name'])
                            send_email(st.session_state.user['email'], "Appointment Confirmation", body, "Appointment System", st.session_state.user['name'])
                            st.success("Appointment accepted and calendar invites sent!")
                
                with col3:
                    if st.button("Reschedule", key=f"reschedule_{appointment['id']}"):
                        new_date = st.text_input("New Date (YYYY-MM-DD)", key=f"date_{appointment['id']}")
                        new_time = st.text_input("New Time (HH:MM)", key=f"time_{appointment['id']}")
                        if st.button("Confirm Reschedule", key=f"confirm_reschedule_{appointment['id']}"):
                            appointment['date'] = new_date
                            appointment['time'] = new_time
                            appointment['status'] = 'rescheduled'
                            save_appointments(appointments)
                            
                            body = f"""Your appointment with Dr. {st.session_state.user['name']} has been rescheduled.<br>
                            <span class="highlight">New Date:</span> {new_date}<br>
                            <span class="highlight">New Time:</span> {new_time}<br>
                            Please confirm the new schedule."""
                            send_email(user['email'], "Appointment Rescheduled", body, st.session_state.user['name'], user['name'])
                            st.success("Appointment rescheduled!")
                    
                    if st.button("Cancel", key=f"cancel_{appointment['id']}"):
                        appointment['status'] = 'cancelled'
                        save_appointments(appointments)
                        
                        body = f"""Your appointment with Dr. {st.session_state.user['name']} has been cancelled."""
                        send_email(user['email'], "Appointment Cancelled", body, st.session_state.user['name'], user['name'])
                        st.success("Appointment cancelled!")
        
        elif st.session_state.user['role'] == 'user':
            st.title("User Dashboard")
            st.subheader("Request Appointment")
            
            doctors = [u for u in users if u['role'] == 'doctor']
            doctor_names = [d['name'] for d in doctors]
            selected_doctor = st.selectbox("Select Doctor", doctor_names)
            date = st.text_input("Date (YYYY-MM-DD)")
            time = st.text_input("Time (HH:MM)")
            
            if st.button("Request Appointment"):
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                    datetime.datetime.strptime(time, '%H:%M')
                    doctor = next(d for d in doctors if d['name'] == selected_doctor)
                    
                    new_appointment = {
                        'id': str(uuid.uuid4()),
                        'user_id': st.session_state.user['id'],
                        'doctor_id': doctor['id'],
                        'date': date,
                        'time': time,
                        'status': 'pending'
                    }
                    appointments.append(new_appointment)
                    save_appointments(appointments)
                    
                    body = f"""A new appointment request from {st.session_state.user['name']}:<br>
                    <span class="highlight">Date:</span> {date}<br>
                    <span class="highlight">Time:</span> {time}<br>
                    Please review and respond to this request."""
                    send_email(doctor['email'], "New Appointment Request", body, st.session_state.user['name'], doctor['name'])
                    st.success("Appointment request sent!")
                    
                except ValueError:
                    st.error("Invalid date or time format")
            
            st.subheader("Your Appointments")
            user_appointments = [a for a in appointments if a['user_id'] == st.session_state.user['id']]
            for appointment in user_appointments:
                doctor = next(u for u in users if u['id'] == appointment['doctor_id'])
                st.write(f"Doctor: {doctor['name']}")
                st.write(f"Date: {appointment['date']}")
                st.write(f"Time: {appointment['time']}")
                st.write(f"Status: {appointment['status']}")
                st.write("---")
                
    # Profile page
    elif page == "Profile":
        st.title("User Profile")
        st.write(f"Name: {st.session_state.user['name']}")
        st.write(f"Email: {st.session_state.user['email']}")
        st.write(f"Role: {st.session_state.user['role']}")
        if st.session_state.user['role'] == 'doctor':
            st.write("Specialization: General Practitioner")  # Example field
            st.write("License Number: DOC123456")  # Example field

if __name__ == "__main__":
    main()