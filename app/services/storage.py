from flask import Flask
from werkzeug.utils import secure_filename
from pathlib import Path
import os

UPLOAD_FOLDER = f'{Path().absolute()}/public/videos'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def save_file_locally(file, folder):
    # Create folder if does not exists
    os.makedirs(UPLOAD_FOLDER+folder, exist_ok=True)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER']+folder, filename))
    return f'{folder}/{filename}'
