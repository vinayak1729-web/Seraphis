from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.services.auth_service import register_user, login_user
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            new_user = register_user(name, email, password)
            session['username'] = name
            session['email'] = email
            session['role'] = new_user['role']
            return redirect('/questionnaire')
        except ValueError as e:
            return render_template('register.html', error=str(e))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        if not identifier or not password:
            return render_template('login.html', error='Please provide all credentials')

        user = login_user(identifier, password)
        if user:
            session['username'] = user['name']
            session['email'] = user['email']
            session['role'] = user.get('role', 'user')

            if session['role'] == 'admin':
                return redirect('/admin/dashboard')
            elif session['role'] == 'doctor':
                return redirect('/doctor/dashboard')
            else:
                return redirect('/home')
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect('/login')

@auth_bp.route('/session-info')
def session_info():
    session_data = dict(session)
    return jsonify(session_data)