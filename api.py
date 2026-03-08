import os
from flask import Flask
from users.routes import users_api

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '123456')
app.register_blueprint(users_api)

