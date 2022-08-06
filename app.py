# from unicodedata import name
# from fashionpedia.fp import FashionPedia
# import numpy as np
# import os
from flask import Flask

app = Flask(__name__)
# img = "../assets/test1.jpg"


@app.route('/')
def test():
    print('aaaa')
    return "Hello"

if __name__ == '__main__':
    app.run()

