#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 23:43:48 2022

@author: rafaelmachado
"""

import os
from joblib import load
import m2cgen
import boto3

### Import environ vars
AWS_BUCKET_MODEL = os.environ['AWS_BUCKET_MODEL']
MODEL_NAME = os.environ['MODEL_NAME']
TEMP_FILE_PATH = '/tmp/' + MODEL_NAME

s3 = boto3.client('s3')
print('Attempt to download file from S3')
s3.download_file(AWS_BUCKET_MODEL, MODEL_NAME, TEMP_FILE_PATH)
print('File successfully downloaded')

# Read downloaded file
with open(TEMP_FILE_PATH, 'rb') as f:
    model = load(f)
    
### Export model
modelStr = m2cgen.export_to_python(model)

modelStr = modelStr.replace('score', 'predict')
modelStr = modelStr.replace('input', 'X')
modelStr = modelStr.replace('var', 'y')

with open('model.py', 'w') as f:
    f.write(modelStr)