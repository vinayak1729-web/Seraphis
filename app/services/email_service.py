import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from flask import current_app

def send_appointment_confirmation(appointment_data, recipient_email=None):
    username = appointment_data.get('patient')
    if not recipient_email:
        user = current_app.mongo_db.users.find_one({'name': username})
        if user:
            recipient_email = user.get('email')
        else:
            current_app.logger.error(f"Could not find email for user: {username}")
            return False

    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASS')

    if not sender_email or not sender_password:
        current_app.logger.error("Email credentials not found in environment variables")
        return False

    appointment_date = appointment_data.get('date')
    appointment_slot = appointment_data.get('slot')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Appointment Confirmation"

    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .email-container {{ max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); margin: auto; }}
            h2 {{ color: #333; text-align: center; }}
            p {{ font-size: 16px; color: #555; line-height: 1.5; }}
            .appointment-details {{ background: #eaf5ff; padding: 10px; border-left: 4px solid #007bff; margin: 15px 0; }}
            .appointment-details strong {{ color: #007bff; }}
            .join-button {{ display: inline-block; background: #007bff; color: white; text-decoration: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; margin-top: 10px; }}
            .join-button:hover {{ background: #0056b3; }}
            .footer {{ font-size: 14px; color: #777; margin-top: 20px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h2>Appointment Confirmation</h2>
            <p>Dear <strong>{username}</strong>,</p>
            <p>Your appointment has been scheduled for:</p>
            <div class="appointment-details">
                <p><strong>Date:</strong> {appointment_date}</p>
                <p><strong>Time:</strong> {appointment_slot}</p>
            </div>
            <p>Click below to join your appointment:</p>
            <p><a href="https://meet.google.com/qeb-uemw-sag" class="join-button">Join Here</a></p>
            <p>Please arrive 10 minutes before your scheduled time.</p>
            <p>If you need to cancel or reschedule, please do so at least 24 hours in advance.</p>
            <p class="footer">Thank you!</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        current_app.logger.info(f"Appointment confirmation email sent to {recipient_email}")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False