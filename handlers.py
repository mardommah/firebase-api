from db import firestore_db

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
    print("data berhasil ditambahkan")


def read_all_data(collection_name):
    doc_ref = firestore_db.collection(collection_name).stream()
    for doc in doc_ref:
        print(f"{doc.id} => {doc.to_dict()}")


def get_data_by_id(collection_name, doc_id):
    doc_ref = firestore_db.collection(collection_name).document(doc_id).get()
    if doc_ref.exists:
        print(f"{doc_ref.id} => {doc_ref.to_dict()}")
    else:
        print("data tidak ditemukan")


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
    print("data berhasil diupdate")


def delete_data(collection_name, doc_id):
    doc_ref = firestore_db.collection(collection_name).document(doc_id)
    doc_ref.delete()
    print("data berhasil dihapus")