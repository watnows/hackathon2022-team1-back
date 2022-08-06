# from unicodedata import name
# from fashionpedia.fp import FashionPedia
import numpy as np
import os
from flask import Flask, request ,send_file
import cv2
import io
from google.cloud import storage
from google.cloud import Blob


app = Flask(__name__)
# img = "../assets/test1.jpg"


@app.route('/')
def test():
    print('aaaa')
    return "Hello"

@app.route('/upload_image',methods = ['GET','POST'])
def upload_image():
    # 画像をとってくる
    if request.files['image']:
        filename = request.files['image'].filename
        content_type = request.files['image'].content_type
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        issuccess,buffer = cv2.imencode('.jpg',img)
        buf = io.BytesIO(buffer)
        buf.seek(0)
        
        # こっから下はfirestorage関連でしゅ
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './fashionpedia-.json'
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('fashionpedia')
        blob = Blob(filename, bucket)
        blob.upload_from_file(data=buf.getvalue(),content_type=content_type)
        
        return send_file(
            buf,attachment_filename=filename,as_attachment=True
        )
        
if __name__ == '__main__':
    app.run()

