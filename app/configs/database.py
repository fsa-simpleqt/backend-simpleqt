import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

import os
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

firebase_url_storageBucket = os.getenv("FIREBASE_URL_STORAGEBUCKET")

# get credentials from .env
credential_firebase = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}

# check if firebase is not initialized
if not firebase_admin._apps:
    # Initialize the app with a service account, granting admin privileges
    cred = credentials.Certificate(credential_firebase)
    firebase_admin.initialize_app(cred, {
        'storageBucket': firebase_url_storageBucket
    })

# Initialize Firestore
firebase_db = firestore.client()
print("Firestore connected")

# Initialize Storage
firebase_bucket = storage.bucket(app=firebase_admin.get_app())
print("Storage connected")
