from flask import Blueprint, render_template, request, jsonify, session,redirect,url_for
from app.services.appointment_service import save_appointment, get_appointments, update_appointment, cancel_appointment, update_appointment_stats, get_appointment_stats, check_appointment_limits
from app.utils.decorators import login_required
from datetime import datetime

appointment_bp = Blueprint('appointment', __name__)

AVAILABLE_SLOTS = ['10:00-11:00', '12:00-13:00', '15:00-16:00', '17:00-18:00']

@appointment_bp.route('/appointment')
@login_required
def appointment():
    if session.get('role') == 'doctor':
        return redirect(url_for('doctor.doctor_dashboard'))
    return render_template('patient_dashboard.html')

@appointment_bp.route('/api/appointments', methods=['GET', 'POST'])
@login_required
def handle_appointments():
    username = session.get('username')

    if request.method == 'GET':
        appointments = get_appointments(username)
        return jsonify(appointments)

    elif request.method == 'POST':
        data = request.json
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d')

        if appointment_date.weekday() >= 5:
            return jsonify({'error': 'No appointments on weekends'}), 400

        can_book, limit_message = check_appointment_limits(username, appointment_date)
        if not can_book:
            return jsonify({'error': limit_message}), 400

        new_appointment = {
            'patient': username,
            'date': data['date'],
            'slot': data['slot'],
            'status': 'pending',
            'patient_email': session.get('email')
        }

        save_appointment(username, new_appointment)
        update_appointment_stats(username, 'booked', appointment_date)
        return jsonify(new_appointment)

@appointment_bp.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@login_required
def update_appointment_route(appointment_id):
    if session.get('role') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401

    doctor_username = session.get('username')
    status = request.json['status']
    result = update_appointment(appointment_id, status, doctor_username)

    if result:
        appointment = result['appointment']
        if status == 'confirmed':
            from app.services.email_service import send_appointment_confirmation
            send_appointment_confirmation(appointment, appointment.get('patient_email'))
        return jsonify({'success': True})
    return jsonify({'error': 'Appointment not found'}), 404

@appointment_bp.route('/api/appointments/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment_route(appointment_id):
    username = session.get('username')
    reason = request.json.get('reason')
    appointment = cancel_appointment(username, appointment_id, reason)

    if appointment:
        appointment_date = datetime.strptime(appointment['date'], '%Y-%m-%d')
        update_appointment_stats(username, 'cancelled', appointment_date)
        return jsonify({'success': True})
    return jsonify({'error': 'Appointment not found'}), 404

@appointment_bp.route('/api/user/stats', methods=['GET'])
@login_required
def get_user_stats():
    username = session.get('username')
    return jsonify(get_appointment_stats(username))

@appointment_bp.route('/api/available-slots', methods=['GET'])
@login_required
def get_available_slots():
    return jsonify(AVAILABLE_SLOTS)