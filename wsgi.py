from app.main import app
import firebase_admin
from firebase_admin import credentials
import os
import json

# Initialize Firebase Admin App
cred = credentials.Certificate({**json.loads(os.environ['FIREBASE_CRED'])})

firebase_admin.initialize_app(cred, {
    'storageBucket': 'web-eye-tracker-front.appspot.com'
})

if __name__ == "__main__":
    app.run(debug=os.environ['FLASK_ENV'])
