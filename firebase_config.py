import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# ✅ Load Firebase credentials from Streamlit Secrets
firebase_secrets = json.loads(st.secrets["firebase"])  # Convert string to dictionary
cred = credentials.Certificate(firebase_secrets)  # Pass parsed dictionary

# ✅ Initialize Firebase (Prevents re-initialization)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# ✅ Firestore Database
db = firestore.client()
