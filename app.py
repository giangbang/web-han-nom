from flask import Flask, render_template, request, redirect
from message import *
import os

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
      print('No file part')
      return render_template('index.html')
    file = request.files['file']
    if file and file.filename != '' and allowed_file(file.filename):
      img_bytes = file.read()
      return success(0)
    print('No selected file')
    return error('[Error]: No attached image or unsupported image extension!')

if __name__ == '__main__':
   app.run(debug=True)