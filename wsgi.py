import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin App
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket':'web-eye-tracker-front.appspot.com'
})

from app.main import app
if __name__ == "__main__":
        app.run()