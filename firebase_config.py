import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Path to your key
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
