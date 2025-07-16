from flask import Blueprint, render_template, redirect, url_for, session
from app.utils.decorators import login_required

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect(url_for('appointment.appointment'))
    return render_template('doctor_dashboard.html')