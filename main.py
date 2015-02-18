# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from hashids import Hashids
from PIL import Image
import subprocess as sp


import dbexe


app = Flask(__name__)

app.config['UPLOADER_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'gif', 'jpg', 'webm', 'mp4'])
app.config['DEBUG'] = True
app.config['DB_NAME'] = "fileshare.db"



full_path_uploads = os.path.join(app.root_path, app.config['UPLOADER_FOLDER'])
full_path_db = os.path.join(app.root_path, app.config['DB_NAME'])

hashids = Hashids(salt="kndwujvncpasiuvbi")
print hashids.encrypt(random.randint(100000000, 9000000000))

int_db = dbexe.MainDb(app.config['DB_NAME'])
print int_db.read_db('name')


def make_pre_image_video(path):
    name = "{0}.png".format(os.path.basename(path))
    full_path_vid_pre = os.path.join(full_path_uploads, name)
    command = [ "ffmpeg", '-i', path, '-vcodec', 'png', '-ss', '10', '-vframes', '1', '-an', '-f', 'rawvideo', full_path_vid_pre ]
    pipe = sp.Popen(command, stdout=sp.PIPE)
    pipe.stdout.readline()
    pipe.terminate()
    make_pre_image(full_path_vid_pre)



def make_pre_image(path):
    if os.path.basename(path).rsplit('.', 1)[1] in set(['webm', 'mp4']):
        make_pre_image_video(path)
    else:
        max_size = 200
        if os.path.basename(path).rsplit('.', 1)[1] not in set(['png', "PNG"]):
            name = "pre_{0}.png".format(os.path.basename(path))
        else:
            name = "pre_{0}".format(os.path.basename(path))
        img = Image.open(path)
        if img.size[0] > img.size[1]:
            wpercent = (max_size / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((max_size, hsize), Image.LANCZOS)
        else:
            hpercent = (max_size / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            img = img.resize((wsize, max_size), Image.LANCZOS)
        img.save(os.path.join(full_path_uploads, name), "PNG")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def check_upload_folder():
    if not os.path.isdir(full_path_uploads):
        os.mkdir(full_path_uploads)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def gallery():
    return render_template('gallery.html', list=int_db.read_db('name'))


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = "{0}.{1}".format(hashids.encrypt(random.randint(1000000000000000000, 9000000000000000000)),
                                    file.filename.rsplit('.', 1)[1])
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
