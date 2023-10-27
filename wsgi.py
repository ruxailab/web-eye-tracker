from app.main import app
import firebase_admin
from firebase_admin import credentials
import os
import json
from decouple import config

# Initialize Firebase Admin App
cred = credentials.Certificate({
    "type": config('EYE_FIREBASE_CRED_TYPE'),
    "project_id": config('EYE_FIREBASE_CRED_PROJECT_ID'),
    "private_key_id": config('EYE_FIREBASE_CRED_PRIVATE_KEY_ID'),
    "private_key": config('EYE_FIREBASE_CRED_PRIVATE_KEY'),
    "client_email": config('EYE_FIREBASE_CRED_CLIENT_EMAIL'),
    "client_id": config('EYE_FIREBASE_CRED_CLIENT_ID'),
    "auth_uri": config('EYE_FIREBASE_CRED_AUTH_URI'),
    "token_uri": config('EYE_FIREBASE_CRED_TOKEN_URI'),
    "auth_provider_x509_cert_url": config('EYE_FIREBASE_CRED_AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": config('EYE_FIREBASE_CRED_CLIENT_CERT_URL'),
})

firebase_admin.initialize_app(cred, {
    'storageBucket': 'web-eye-tracker-front.appspot.com'
})

if __name__ == "__main__":
    app.run(debug=os.environ['FLASK_ENV'])
