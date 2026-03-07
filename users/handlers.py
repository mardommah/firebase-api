from utils.db import firestore_db
from utils.response import create_response

# sintaks dasar untuk menambahkan data ke firestore
'''
.document() -> generate id otomatis
.document("id") -> generate id manual
'''
def add_data(collection_name, datas):
    # isi collection name sesuai yang dituju, cotoh "users"
    doc_ref = firestore_db.collection(collection_name).document()

    # olah data dari paramter dan simpan ke firebase
    '''
    sample data:

    data = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }
    '''
    
    doc_ref.set(datas)
    return create_response(200, "berhasil menambahkan data", datas)


def read_all_data(collection_name):
    doc_ref = firestore_db.collection(collection_name).stream()
    datas = []
    for doc in doc_ref:
        datas.append(doc.to_dict())
    return create_response(200, "berhasil get data", datas)


def get_data_by_id(collection_name, doc_id):
    doc_ref = firestore_db.collection(collection_name).document(doc_id).get()
    if doc_ref.exists:
        return create_response(200, "berhasil get data", doc_ref.to_dict())
    else:
        return create_response(404, "data tidak ditemukan")


def update_data(collection_name, doc_id, new_data):
    doc_ref = firestore_db.collection(collection_name).document(doc_id)

    '''
    Format data update
    new_data = {
        "name": "Jane Doe",
        "age": 25
    }
    '''
    doc_ref.update(new_data)
    return create_response(200, "berhasil update data", new_data)


def delete_data(collection_name, doc_id):
    doc_ref = firestore_db.collection(collection_name).document(doc_id)
    doc_ref.delete()
    return create_response(200, "berhasil hapus data")
