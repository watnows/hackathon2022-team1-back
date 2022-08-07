import numpy as np
# import os
from flask import Flask, request ,send_file
import cv2
import io
import firebase_admin
from flask_cors import CORS

from firebase_admin import credentials
from google.cloud import storage
# from google.cloud.storage import Blob
app = Flask(__name__)
app.config['DEBUG'] = True
# img = "../assets/test1.jpg"
CORS(app)

JSON_PATH = 'fashionmonster-b8b0c-firebase-adminsdk-q6k3r-bc0409b1e9.json'
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)

@app.route('/')
def test():
    print('aaaa')
    return "Hello"

@app.route('/testing',methods=['GET','POST'])
def testing():
    return "Hello"
# JSON_PATH = 'fashionmonster-b8b0c-firebase-adminsdk-q6k3r-bc0409b1e9.json'
# cred = credentials.Certificate(JSON_PATH)
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# firebase = pyrebase.initialize_app(config)
# cred = credentials.Certificate("./fashionmonster-b8b0c-firebase-adminsdk-q6k3r-bc0409b1e9.json")
# firebase_admin.initialize_app(cred,{
#     'storageBucket':'fashionmonster-b8b0c.appspot.com'
# })
# bucket = storage.bucket('Test')
# default_app=firebase_admin.initialize_app(cred,{'storageBucket': 'fashionmonster-b8b0c.appspot.com'})
@app.route("/final_recive",methods=['GET','POST'])
def image():
    # string
    filename = request.files['image'].filename
    # string
    content_type = request.files['image'].content_type
    # string
    stream = request.files['image'].stream
    # number
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    try:
        # np.asarray
        img = cv2.imdecode(img_array, 1)
        # tupple
        # (True, array([255, 216, 255, ..., 127, 255, 217], dtype=uint8))
        is_success,buffer = cv2.imencode('.jpg',img)
        
        buf = io.BytesIO(buffer)
        buf.seek(0)
        
        return send_file(
            buf,as_attachment=True,download_name=filename)
        
        # return send_file(
        #     buf,as_attachment=True,attachment_filename=filename
        # )
        
    except Exception as e:
        print(e)
        return 'Error'

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
        
        gcs = storage.Client()
        bucket = gcs.get_bucket('fashionmonster-b8b0c.appspot.com')
        blob = bucket.blob(buf.filename)
        
    

if __name__ == '__main__':
    app.run(debug=True)