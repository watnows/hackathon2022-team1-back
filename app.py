# from unicodedata import name
# from fashionpedia.fp import FashionPedia
from os import abort
import numpy as np
import os
from flask import Flask, request ,send_file
import cv2
import io
import firebase_admin
from flask_cors import CORS
from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import storage
# import pyrebas\e

# from PIL import Image
# import inspect
# from google.cloud import storage
# from google.cloud import Blob

app = Flask(__name__)
# img = "../assets/test1.jpg"
CORS(app)


@app.route('/')
def test():
    print('aaaa')
    return "Hello"

@app.route('/testing',methods=['GET','POST'])
def testing():
    return "Hello"

# firebase = pyrebase.initialize_app(config)
 
# db = firebase.database()
# GOOGLE_APPLICATION_CREDENTIALS=os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
# FIREBASE_STORAGE_BUCKET=os.environ["FIREBASE_STORAGE_BUCKET"]

# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
# firebase_admin.initialize_app(cred,{'storageBucket':FIREBASE_STORAGE_BUCKET})
# bucket = storage.bucket()

@app.route('/recive_img',methods=['GET','POST'])
def recive_image():
    try:
        img_dir = 'static/imgs/'
        if request.method=='GET':
            img_path =None
        elif request.method == 'POST':
            stream = request.files['img'].stream
            img_array = np.asarray(bytearray(stream.read()),dtype=np.uint8)
            img = cv2.imdecode(img_array,1)
            img_path = img_dir +".jpg"
            cv2.imwrite(img_path,img)
            
            # storage_client = storage.Client()
            # # bucket = storage_client.bucket(FIREBASE_STORAGE_BUCKET)
            # blob =  bucket.blob(img_path)
            # blob.upload_from_filename(img_path)
            
        return 'HEllo'
    except Exception as e:
        print(e)
        # abort(e.code)
    return send_file


@app.route('/upload_image',methods = ['GET','POST'])
def upload_image():
    # 画像をとってくる
    if request.files['image']:
        # streamはデータの入出力を行うためのやつ
        filename = request.files['image'].filename
        content_type = request.files['image'].content_type
        # 画像として読み込み
        stream = request.files['image'].stream
        # numpy形式に変換.asarray配列になる
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        # 画像のデコード
        img = cv2.imdecode(img_array, 1)
        # jpgにデコード
        issuccess,buffer = cv2.imencode('.jpg',img)
        # バイトをいろいろ
        buf = io.BytesIO(buffer)
        buf.seek(0)
        
        # こっから下はfirestorage関連でしゅ
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './fashionpedia-.json'
        # storage_client = storage.Client()
        # bucket = storage_client.get_bucket('fashionpedia')
        # blob = Blob(filename, bucket)
        # blob.upload_from_file(data=buf.getvalue(),content_type=content_type)
        
        return send_file(
            buf,attachment_filename=filename,as_attachment=True
        )

        

if __name__ == '__main__':
    app.run(debug=True)