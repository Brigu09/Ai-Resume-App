import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Load Firebase credentials directly from Streamlit Secrets (No JSON conversion needed)
firebase_secrets = st.secrets["firebase"]
cred = credentials.Certificate(firebase_secrets)  # Pass dictionary directly

# Initialize Firebase (Prevent re-initialization)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore Database
db = firestore.client()
