import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("creds.json")

# inisialisasi aplikasi firebase
firebase_admin.initialize_app(credential=cred)

# inisilisasi firestore client
firestore_db = firestore.client()

print("Database connected successfully!")


# test tambah data