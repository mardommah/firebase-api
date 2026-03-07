from flask import Flask

from users.routes import users_api

app = Flask(__name__)
app.register_blueprint(users_api)