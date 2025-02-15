import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Load Firebase credentials from Streamlit Secrets
firebase_secrets = st.secrets["firebase"]
cred = credentials.Certificate(json.loads(json.dumps(firebase_secrets)))

# Initialize Firebase
if not firebase_admin._apps:  # Prevents duplicate initialization
    firebase_admin.initialize_app(cred)

# Firestore Database
db = firestore.client()
