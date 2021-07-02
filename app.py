from flask import Flask, render_template, request, redirect
from message import *
import os
import pandas as pd
import numpy as np  

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def get_prediction():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    if 'file' not in request.files: 
      return error('[Error]: No file part')
    file = request.files['file']
    if file and file.filename != '' and allowed_file(file.filename):
      img_bytes = file.read()
      ann = pd.read_csv('test/LienPhai-2484.txt',header=None).to_numpy().astype(np.float32)
      ann = (ann*500/3563).astype(np.int16)[..., :8].tolist()
      return success(ann)
    return error('[Error]: Unsupported file extension!')

if __name__ == '__main__':
   app.run(debug=True)