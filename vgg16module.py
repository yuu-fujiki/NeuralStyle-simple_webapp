# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 14:26:44 2017

@author: Kobayashi
"""
from module import Module
from flask import Flask, request, render_template
from keras.models import load_model
import os
from keras.preprocessing import image
import numpy as np
from werkzeug.utils import secure_filename
import json
import math
import config

import scipy
import scipy.io
import scipy.misc
from style_transfer import StyleTransfer

#TODO 変な拡張子のファイルをアップロードできないようにする。

class vgg16module(Module):
    def __init__(self, **kwargs):
        super(vgg16module, self).__init__()
        self.model_path = kwargs.get('model_path', os.getcwd())
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = kwargs.get('UPLOAD_FOLDER',
                       os.path.join(os.getcwd()))
        # with open('indices.txt') as j:
        #     self.class_indices = {v: k for k, v in json.load(j).items()}

        self.base_dir = kwargs.get('base_dir', os.getcwd())
        self.image_rows = kwargs.get('image_rows', 300)
        self.image_cols = kwargs.get('image_cols', 400)

    def run(self):
        """
        apiサーバを動かす。
        """

        # model = load_model(os.path.join(self.base_dir, 'finetune.h5'))

        @self.app.route('/', methods=['POST'])
        def predict():
            content_img = request.files['content']
            #filename = secure_filename(file.filename)
            content_img.save(os.path.join(self.app.config['UPLOAD_FOLDER'], 'content_img'))
            content_img = image.load_img(
                    os.path.join(self.app.config['UPLOAD_FOLDER'], 'content_img'),
                    target_size=(self.image_rows, self.image_cols))
            content_img = image.img_to_array(content_img)

            style_img = request.files['style']
            style_img.save(os.path.join(self.app.config['UPLOAD_FOLDER'], 'style_img'))
            style_img = image.load_img(
                    os.path.join(self.app.config['UPLOAD_FOLDER'], 'style_img'),
                    target_size=(self.image_rows, self.image_cols))
            style_img = image.img_to_array(style_img)

            pretrained_model_dir_path = './pretrained-model'

            vgg19_model_path = pretrained_model_dir_path + " /imagenet-vgg-verydeep-19.mat"
            ss = StyleTransfer(vgg19_model_path)

            generated_image = ss.fit_and_transform(content_img, style_img, output_dir_path='./static', num_iterations=1)
            generated_image = np.reshape(generated_image,(300, 400, 3))
            generated_image = image.array_to_img(generated_image)
            return render_template('index.html', message='This is a generated image')

        port = config.port
        self.app.run(port=port)
