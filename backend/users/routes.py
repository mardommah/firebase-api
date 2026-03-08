from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from backend.users.handlers import (
    handle_users_data, handle_manage_user, handle_my_subjects,
    user_login, user_register
)
from backend.subjects.routes import admin_required
from functools import wraps

users_api = Blueprint('users_api', __name__)


# Middleware untuk proteksi route yang membutuhkan login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Silakan login terlebih dahulu', 'error')
            return redirect(url_for('users_api.login'))
        return f(*args, **kwargs)
    return decorated_function


@users_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return user_login(email, password)
    return render_template('users/login.html')


@users_api.route('/dashboard')
@login_required
def dashboard():
    if session.get('user_role') == 'admin':
        return redirect(url_for('users_api.admin_dashboard'))
    return redirect(url_for('users_api.user_dashboard'))


@users_api.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if session.get('user_role') != 'admin':
        flash('Akses ditolak', 'error')
        return redirect(url_for('users_api.user_dashboard'))
    return render_template('users/admin_dashboard.html')


@users_api.route('/user/dashboard')
@login_required
def user_dashboard():
    return render_template('users/user_dashboard.html')


@users_api.route('/logout')
def logout():
    session.clear()
    return render_template('users/logout.html')


@users_api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        return user_register(name, email, password, confirm_password)
    return render_template('users/register.html')


@users_api.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users_data():
    return handle_users_data()


@users_api.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def manage_user(user_id):
    return handle_manage_user(user_id)


@users_api.route('/my-subjects', methods=['GET', 'POST'])
@login_required
def my_subjects():
    return handle_my_subjects()