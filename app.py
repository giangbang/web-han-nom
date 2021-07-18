from flask import Flask, render_template, request, redirect
from message import *
import os
import pandas as pd
import numpy as np  
from demo import Demo
import torch
import cv2
from experiment import Structure, Experiment
from concern.config import Configurable, Config
import math

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
      args = {'exp': 'experiments/seg_detector/td500_resnet18_deform_thre.yaml', 
              'resume': 'weights/final', 'image_path': 'test/' + file.filename, 
              'result_dir': './demo_results/', 'image_short_side': 736, 'box_thresh': 0.6, 'visualize': True, 
              'resize': False, 'polygon': False, 'eager_show': False}
      #convert string data to numpy array
      npimg = np.frombuffer(img_bytes, np.uint8)
      # convert numpy array to image
      img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
      conf = Config()
      experiment_args = conf.compile(conf.load(args['exp']))['Experiment']
      experiment_args.update(cmd=args)
      experiment = Configurable.construct_class_from_config(experiment_args)
      ann = Demo(experiment, experiment_args, cmd=args).inference(args['image_path'], args['visualize'])
      ann =  ann.reshape((ann.shape[0], -1))
      # ann = pd.read_csv('test/LienPhai-2484.txt',header=None).to_numpy().astype(np.float32)
      ann = ann.astype(float)
      ann = (ann*500/img.shape[0]).astype(np.int16)[..., :8].tolist()
      return success(ann)
    return error('[Error]: Unsupported file extension!')

if __name__ == '__main__':
   app.run(debug=True)