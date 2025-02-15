import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firebase (Prevents re-initialization)
if not firebase_admin._apps:
    # Get Firebase credentials directly from Streamlit secrets
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

# Firestore Database
db = firestore.client()
