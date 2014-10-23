import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import sqlite3


app = Flask(__name__)

app.config['UPLOADER_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'mp4'])
app.config['DEBUG'] = True
app.config['DB_NAME'] = "fileshare.db"

full_path_uploads = os.path.join(app.root_path, app.config['UPLOADER_FOLDER'])
full_path_db = os.path.join(app.root_path, app.config['DB_NAME'])





def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

def check_upload_folder():
    if not os.path.isdir(full_path_uploads):
        os.mkdir(full_path_uploads)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOADER_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(full_path_uploads, filename)


if __name__ == '__main__':
    check_upload_folder()
    app.run()
