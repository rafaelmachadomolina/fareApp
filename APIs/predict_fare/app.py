#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:48:50 2022

@author: rafaelmachado
"""

### Import modules
import os
import json
import boto3
from joblib import load

### Import environ vars
AWS_BUCKET_MODEL = os.environ['AWS_BUCKET_MODEL']
MODEL_NAME = os.environ['MODEL_NAME']
TEMP_FILE_PATH = '/tmp/' + MODEL_NAME

### Tests
# with open('simpleEvent.json', 'r') as f:
#     event = json.load(f)

### Functions
def get_model(TEMP_FILE_PATH):
    s3 = boto3.client('s3')
    print('Attempt to download file from S3')
    s3.download_file(AWS_BUCKET_MODEL, MODEL_NAME, TEMP_FILE_PATH)
    print('File successfully downloaded')
    
    # Read downloaded file
    with open(TEMP_FILE_PATH, 'rb') as f:
        pipeline = load(f)
        
    return pipeline;

### Execute pipeline
def execute_model(model, X):
    y = model.predict(X)
    
    return round(y[0], 2);


def handler(event, context):
    
    # Define responses
    response_bad = {"statusCode": 400,
                    "body": None}
    
    # Get data from the event
    X = [event['features']]
    
    # Load pipeline
    try:
        model = get_model(TEMP_FILE_PATH)
        print('Pipeline imported successfully')
        
    except Exception as e:
        print('Something went wrong loading the pipeline')
        print('Exception:', e)
        return json.dumps(response_bad)
        
    #Execute pipeline
    try:
        body = execute_model(model, X)
        print('Pipeline correctly executed')
        
    except ValueError as e:
        print('Value error:', e)
        return json.dumps(response_bad)
        
    except Exception as e:
        print('Something went wrong with the pipeline execution')
        print('Exception:', e)
        return json.dumps(response_bad)
        
    # Send transformed data in the response
    try:
        
        response_good = {"statusCode": 200,
                        "body": body}
        
        return json.dumps(response_good)
        
    except Exception as e:
        print('Oh oh, something went wrong with the call')
        print('Error message:', e)
        
        return json.dumps(response_bad)
        
    finally:
        print('API call finalised.')
   