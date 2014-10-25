# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from hashids import Hashids
import dbexe
import random
import Image

app = Flask(__name__)

app.config['UPLOADER_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'mp4'])
app.config['DEBUG'] = True
app.config['DB_NAME'] = "fileshare.db"

full_path_uploads = os.path.join(app.root_path, app.config['UPLOADER_FOLDER'])
full_path_db = os.path.join(app.root_path, app.config['DB_NAME'])

hashids = Hashids(salt="kndwujvncpasiuvbi")
print hashids.encrypt(random.randint(100000000, 9000000000))

int_db = dbexe.MainDb(app.config['DB_NAME'])

def make_pre_image(path):
    basewidth = 300
    name = "pre_{0}".format(os.path.basename(path))
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(os.path.join(full_path_uploads, name))

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
            filename = "{0}.{1}".format(hashids.encrypt(random.randint(1000000000000000000, 9000000000000000000)), file.filename.rsplit('.',1)[1])
            full_path_name = os.path.join(app.root_path, app.config['UPLOADER_FOLDER'], filename)
            file.save(full_path_name)
            int_db.insert_files(filename, full_path_name, "/uploads/{0}".format(filename))
            make_pre_image(full_path_name)
            return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(full_path_uploads, filename)


if __name__ == '__main__':
    check_upload_folder()
    app.run()
