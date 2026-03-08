import os
from flask import Flask, render_template
from backend.users.routes import users_api
from backend.subjects.routes import subjects_api

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '123456')
app.register_blueprint(users_api)
app.register_blueprint(subjects_api)


@app.route('/')
def index():
    return render_template('users/welcome.html')

