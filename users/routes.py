from flask import Flask, request, Blueprint
from users.handlers import add_data, read_all_data, update_data, get_data_by_id, delete_data

users_api = Blueprint('users_api', __name__)


@users_api.route('/users', methods=['GET', 'POST'])
def users_data():
    if request.method == 'POST':
        data = request.get_json()
        # insert user data
        return add_data("users", data)
    else:
        return read_all_data("users")

@users_api.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    if request.method == 'PUT':
        new_data = request.get_json()
        return update_data("users", user_id, new_data)
    elif request.method == 'DELETE':
        return delete_data("users", user_id)
    else:
        return get_data_by_id("users", user_id)