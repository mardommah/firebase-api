from flask import render_template, session, flash, redirect, url_for, request
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


def handle_users_data():
    if request.method == 'POST':
        data = request.get_json()
        return add_data(data)
    else:
        return render_template('users/users.html', users=read_all_data()['data'])


def handle_manage_user(user_id):
    if request.method == 'PUT':
        new_data = request.get_json()
        return update_data(user_id, new_data)
    elif request.method == 'DELETE':
        return delete_data(user_id)
    else:
        return get_data_by_id(user_id)


def handle_my_subjects():
    user_id = session.get('user_id')
    if request.method == 'POST':
        subject_ids = request.form.getlist('subjects')
        subjects_ref = firestore_db.collection('user_subjects')
        # Hapus data lama
        old_docs = subjects_ref.where('user_id', '==', user_id).stream()
        for doc in old_docs:
            doc.reference.delete()
        # Simpan data baru
        for subject_id in subject_ids:
            subjects_ref.document().set({
                'user_id': user_id,
                'subject_id': subject_id
            })
        flash('Mata pelajaran berhasil disimpan', 'success')
        return redirect(url_for('users_api.my_subjects'))

    # Ambil semua mata pelajaran
    subjects_ref = firestore_db.collection('subjects')
    all_subjects = []
    for doc in subjects_ref.stream():
        data = doc.to_dict()
        data['id'] = doc.id
        all_subjects.append(data)

    # Ambil mata pelajaran yang sudah dipilih user
    user_subjects_ref = firestore_db.collection('user_subjects')
    user_subjects_docs = user_subjects_ref.where('user_id', '==', user_id).stream()
    selected_ids = [doc.to_dict()['subject_id'] for doc in user_subjects_docs]

    return render_template('users/my_subjects.html', subjects=all_subjects, selected_ids=selected_ids)


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

        # Cek apakah admin terdaftar di collection admins
        admins_ref = firestore_db.collection("admins")
        admin_doc = admins_ref.where("email", "==", email).get()

        if admin_doc:
            session['user_role'] = 'admin'
        else:
            session['user_role'] = user.get('role', 'user')

        flash('Login berhasil!', 'success')

        # Redirect berdasarkan role
        if session['user_role'] == 'admin':
            return redirect(url_for('users_api.admin_dashboard'))
        else:
            return redirect(url_for('users_api.user_dashboard'))
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
            'password': generate_password_hash(password),
            'role': 'user'  # Default role untuk user baru
        })
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('users_api.login'))
    else:
        flash('Semua field harus diisi!', 'error')
        return redirect(url_for('users_api.register'))