from utils.db import firestore_db
from werkzeug.security import generate_password_hash
from utils.response import create_response


def check_user_exist(collection, email):
    doc_ref = firestore_db.collection(collection).where("email", "==", email).get()

    if len(doc_ref) > 0:
        return create_response(200, "users sudah terdaftar", doc_ref[0].to_dict())
    else:
        return create_response(404, "users tidak ditemukan")

def create_user_account(collection, data):
    # field wajid: email & password

    if "email" not in data or "password" not in data:
        return create_response(400)

    doc_ref = firestore_db.collection(collection).document()
    data["password"] = generate_password_hash(data["password"])

    # cek jika email sudah terdaftar
    check_email = check_user_exist(collection=collection, email=data["email"])

    if check_email.status_code == 200:
        return check_email
    
    doc_ref.set(data)
    return create_response(200, "berhasil membuat akun", data)
