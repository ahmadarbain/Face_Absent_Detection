from flask import Flask, render_template, redirect, url_for
from captureImg import WebcamApp
import os
from firebase_admin import credentials, db, initialize_app
import firebase_admin
from flask import send_from_directory
import main  # Import modul main

app = Flask(__name__)

UPLOAD_FOLDER = 'RawImages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {
        'databaseURL': 'https://faceemployeeattandance-default-rtdb.firebaseio.com/'
    })

ref = db.reference('Attendance')
attendance = ref.get()

@app.route('/')
def index():
    latest_image = None
    folder_path = app.config['UPLOAD_FOLDER']
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        if files:
            latest_image = sorted(files)[-1]
    return render_template('index.html', image_filename=latest_image, attendance=attendance)

@app.route('/start_detection', methods=['POST'])
def start_detection():
    # Panggil fungsi capture_video() dari modul main saat tombol diklik
    main.capture_video()
    return redirect(url_for('index'))

@app.route('/start_capture', methods=['POST'])
def start_capture():
    webcam_app = WebcamApp(None, None)
    webcam_app.capture_image()
    return redirect(url_for('index'))

@app.route('/raw_images/<path:filename>')
def raw_images(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
