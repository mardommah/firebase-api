from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from utils.db import firestore_db
from utils.response import create_response

subjects_api = Blueprint('subjects_api', __name__)

doc_ref = firestore_db.collection("subjects")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini', 'error')
            return redirect(url_for('users_api.user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@subjects_api.route('/subjects', methods=['GET', 'POST'])
@admin_required
def subjects_data():
    if request.method == 'POST':
        try:
            data = request.get_json()
            doc_ref.document().set(data)
            return create_response(200, "berhasil menambahkan data", data)
        except Exception as e:
            return create_response(500, f"Gagal menambahkan data: {str(e)}"), 500
    else:
        subjects = []
        docs = doc_ref.stream()
        for i, doc in enumerate(docs):
            data = doc.to_dict()
            data['id'] = doc.id
            data['no'] = i + 1
            subjects.append(data)
        return render_template('subjects/subjects.html', subjects=subjects)


@subjects_api.route('/subject/<subject_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def manage_subject(subject_id):
    if request.method == 'PUT':
        new_data = request.get_json()
        doc_ref.document(subject_id).update(new_data)
        return create_response(200, "berhasil update data", new_data)
    elif request.method == 'DELETE':
        doc_ref.document(subject_id).delete()
        return create_response(200, "berhasil hapus data")
    else:
        doc = doc_ref.document(subject_id).get()
        if doc.exists:
            return create_response(200, "berhasil get data", doc.to_dict())
        return create_response(404, "data tidak ditemukan")
