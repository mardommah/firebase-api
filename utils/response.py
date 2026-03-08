def create_response(status_code, message, data=None):
    response = {
        "code": status_code,
        "message": message,
        "data": data
    }

    return response