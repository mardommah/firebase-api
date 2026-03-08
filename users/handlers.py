from flask import render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import firestore_db
from utils.response import create_response

# sintaks dasar untuk menambahkan data ke firestore
'''
.document() -> generate id otomatis
.document("id") -> generate id manual
'''

doc_ref = firestore_db.collection("users")

def add_data(datas):
    # olah data dari paramter dan simpan ke firebase
    '''
    sample data:

    data = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }
    '''
    
    doc_ref.document().set(datas)
    return create_response(200, "berhasil menambahkan data", datas)


def read_all_data():
    doc_ref_data = doc_ref.stream()
    datas = []
    for doc in doc_ref_data:
        # tambahkan key id untuk menyimpan id user
        data = doc.to_dict()
        data['id'] = doc.id
        # tampilkan nomor urut data
        data["no"] = len(datas) + 1
        datas.append(data)
    return create_response(200, "berhasil get data", datas)


def get_data_by_id(doc_id):
    doc_ref_data = doc_ref.document(doc_id).get()
    if doc_ref_data.exists:
        return create_response(200, "berhasil get data", doc_ref_data.to_dict())
    else:
        return create_response(404, "data tidak ditemukan")


def update_data(doc_id, new_data):
    doc_ref_data = doc_ref.document(doc_id)

    '''
    Format data update
    new_data = {
        "name": "Jane Doe",
        "age": 25
    }
    '''
    if not doc_ref_data.get().exists:
        return create_response(404, "data tidak ditemukan")
    
    doc_ref_data.update(new_data)
    return create_response(200, "berhasil update data", new_data)


def delete_data(doc_id):
    docr_ref_data = doc_ref.document(doc_id)
    if not docr_ref_data.get().exists:
        return create_response(404, "data tidak ditemukan")

    docr_ref_data.delete()
    return create_response(200, "berhasil hapus data")


def user_login(email, password):
    # Cari user berdasarkan email di database
    users = doc_ref.where("email", "==", email).stream()
    user = None
    for doc in users:
        user = doc.to_dict()
        user['id'] = doc.id
        break

    # Verifikasi email dan password
    if user and check_password_hash(user['password'], password):
        session['user_email'] = email
        session['user_id'] = user['id']
        flash('Login berhasil!', 'success')
        return redirect(url_for('users_api.users_data'))
    else:
        flash('Email atau password salah', 'error')
        return redirect(url_for('users_api.login'))


def user_register(name, email, password, confirm_password):
    if password != confirm_password:
        flash('Password tidak cocok!', 'error')
        return redirect(url_for('users_api.register'))

    # Simpan user baru ke database
    if name and email and password:
        add_data({
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        })
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('users_api.login'))
    else:
        flash('Semua field harus diisi!', 'error')
        return redirect(url_for('users_api.register'))