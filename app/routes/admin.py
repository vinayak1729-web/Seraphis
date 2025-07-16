from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from app.services.auth_service import load_users, register_user
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect('/login')

    if session.get('role') != 'admin':
        flash('Access restricted. Admin privileges required.', 'error')
        return redirect('/')

    users = load_users()
    current_admin = session['email']
    return render_template('admin_dashboard.html', users=users, current_admin=current_admin)

@admin_bp.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if 'email' not in session or session.get('role') != 'admin':
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        try:
            new_user = register_user(name, email, password)
            new_user['role'] = role
            new_user['created_by'] = session['email']
            current_app.mongo_db.users.update_one(
                {'email': email},
                {'$set': {'role': role, 'created_by': session['email']}}
            )
            return redirect('/admin/dashboard')
        except ValueError as e:
            return render_template('create_user.html', error=str(e))

    return render_template('create_user.html')

@admin_bp.route('/admin/update_role/<user_email>', methods=['POST'])
def update_role(user_email):
    if 'email' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    new_role = request.form.get('new_role')
    if not new_role or new_role not in ['user', 'admin', 'doctor']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400

    user = current_app.mongo_db.users.find_one({'email': user_email})
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    current_app.mongo_db.users.update_one(
        {'email': user_email},
        {'$set': {'role': new_role, 'updated_at': datetime.now().isoformat(), 'updated_by': session['email']}}
    )
    return jsonify({'success': True, 'message': 'Role updated successfully'})