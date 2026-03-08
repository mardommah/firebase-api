from flask import Flask, request, Blueprint, render_template, redirect, url_for, flash, session
from users.handlers import add_data, read_all_data, update_data, get_data_by_id, delete_data, user_login, user_register
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
def users_data():
    if request.method == 'POST':
        data = request.get_json()
        # insert user data
        return render_template('users/users.html', users=data)
    else:
        return render_template('users/users.html', users=read_all_data()['data'])

@users_api.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_user(user_id):
    if request.method == 'PUT':
        new_data = request.get_json()
        return update_data(user_id, new_data)
    elif request.method == 'DELETE':
        return delete_data(user_id)
    else:
        return get_data_by_id( user_id)