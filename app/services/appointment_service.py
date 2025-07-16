from datetime import datetime, timedelta
from flask import current_app
from app.services.email_service import send_appointment_confirmation

def save_appointment(username, appointment_data):
    appointments_col = current_app.mongo_db.appointments
    appointment_data['id'] = appointments_col.count_documents({}) + 1
    appointment_data['created_at'] = datetime.now().isoformat()
    appointments_col.insert_one(appointment_data)
    send_appointment_confirmation(appointment_data, appointment_data.get('patient_email'))

def get_appointments(username):
    appointments_col = current_app.mongo_db.appointments
    return list(appointments_col.find({'patient': username}))

def update_appointment(appointment_id, status, doctor_username):
    appointments_col = current_app.mongo_db.appointments
    doctor_appointments_col = current_app.mongo_db.doctor_appointments

    appointment = appointments_col.find_one({'id': appointment_id})
    if not appointment:
        return None

    appointments_col.update_one(
        {'id': appointment_id},
        {'$set': {'status': status}}
    )

    appointment['status'] = status
    patient_username = appointment['patient']
    patient_info = current_app.mongo_db.user_data.find_one({'username': patient_username}) or {}

    new_doctor_appointment = {
        'appointment_id': appointment_id,
        'patient': patient_username,
        'patient_email': appointment.get('patient_email'),
        'date': appointment['date'],
        'slot': appointment['slot'],
        'status': status,
        'patient_info': patient_info,
        'updated_at': datetime.now().isoformat()
    }

    doctor_appointments_col.update_one(
        {'appointment_id': appointment_id, 'patient': patient_username},
        {'$set': new_doctor_appointment},
        upsert=True
    )

    return {'appointment': appointment}

def cancel_appointment(username, appointment_id, reason):
    appointments_col = current_app.mongo_db.appointments
    appointment = appointments_col.find_one({'id': appointment_id, 'patient': username})
    if appointment:
        appointments_col.update_one(
            {'id': appointment_id, 'patient': username},
            {'$set': {'status': 'cancelled', 'cancellation_reason': reason}}
        )
        return appointment
    return None

def update_appointment_stats(username, action, date):
    stats_col = current_app.mongo_db.appointment_stats
    stats = stats_col.find_one({'username': username}) or {
        'username': username,
        'total_appointments': 0,
        'total_cancellations': 0,
        'yearly_stats': {},
        'monthly_stats': {},
        'rating': 'white'
    }

    year = str(date.year)
    month = str(date.month)

    if year not in stats['yearly_stats']:
        stats['yearly_stats'][year] = {'booked': 0, 'cancelled': 0}
    if month not in stats['monthly_stats']:
        stats['monthly_stats'][month] = {'booked': 0, 'cancelled': 0}

    if action == 'booked':
        stats['total_appointments'] += 1
        stats['yearly_stats'][year]['booked'] += 1
        stats['monthly_stats'][month]['booked'] += 1
    elif action == 'cancelled':
        stats['total_cancellations'] += 1
        stats['yearly_stats'][year]['cancelled'] += 1
        stats['monthly_stats'][month]['cancelled'] += 1

    monthly_cancel_rate = stats['monthly_stats'][month]['cancelled'] / max(stats['monthly_stats'][month]['booked'], 1)
    stats['rating'] = 'blue' if monthly_cancel_rate < 0.1 else 'red' if monthly_cancel_rate > 0.4 else 'white'

    stats_col.update_one(
        {'username': username},
        {'$set': stats},
        upsert=True
    )

def get_appointment_stats(username):
    stats_col = current_app.mongo_db.appointment_stats
    stats = stats_col.find_one({'username': username})
    if not stats:
        stats = {
            'username': username,
            'total_appointments': 0,
            'total_cancellations': 0,
            'yearly_stats': {},
            'monthly_stats': {},
            'rating': 'white'
        }
    return stats

def check_appointment_limits(username, appointment_date):
    appointments = list(current_app.mongo_db.appointments.find({'patient': username, 'status': {'$ne': 'cancelled'}}))
    week_start = appointment_date - timedelta(days=appointment_date.weekday())
    week_end = week_start + timedelta(days=6)
    week_appointments = [a for a in appointments if week_start <= datetime.strptime(a['date'], '%Y-%m-%d') <= week_end]
    if len(week_appointments) >= 1:
        return False, "Weekly limit reached (maximum 1 appointment per week)"

    month_start = appointment_date.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    month_appointments = [a for a in appointments if month_start <= datetime.strptime(a['date'], '%Y-%m-%d') <= month_end]
    if len(month_appointments) >= 4:
        return False, "Monthly limit reached (maximum 4 appointments per month)"

    return True, None