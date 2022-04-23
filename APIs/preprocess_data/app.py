#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:48:50 2022

@author: rafaelmachado
"""

### Import modules
import os
import json
import pickle
import boto3

### Import environ vars
AWS_BUCKET_MODEL = os.environ['AWS_BUCKET_MODEL']
PIPELINE_NAME = os.environ['PIPELINE_NAME']
TEMP_FILE_PATH = '/tmp/' + PIPELINE_NAME

# Functions
def get_pipeline(TEMP_FILE_PATH):
    s3 = boto3.client('s3')
    s3.download_file(AWS_BUCKET_MODEL, PIPELINE_NAME, TEMP_FILE_PATH)
    
    # Read downloaded file
    with open(TEMP_FILE_PATH, 'rb') as f:
        pipeline = pickle.load(f)
        
    return pipeline;

# Execute pipeline
def execute_pipeline(pipeline, X):
    X_t = pipeline.transform(X)
    X_t = [i for i in X_t[0]]
    return X_t;


def handler(event, context):
    
    # Define responses
    response_bad = {"statusCode": 400,
                    "body": None}
    
    # Get data from the event
    X = [event['record']]
    
    # Load pipeline
    try:
        pipeline = get_pipeline(TEMP_FILE_PATH)
        print('Pipeline imported successfully')
        
    except Exception as e:
        print('Something went wrong loading the pipeline')
        print('Exception:', e)
        return json.dumps(response_bad)
        
    #Execute pipeline
    try:
        body = execute_pipeline(pipeline, X)
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
        if(len(body) != 12): # Checks that the output has the corret length
            raise Exception('Wrong length of response')

        response_good = {"statusCode": 200,
                        "body": body}
        
        return json.dumps(response_good)
        
    except Exception as e:
        print('Oh oh, something went wrong with the call')
        print('Error message:', e)
        
        return json.dumps(response_bad)
        
    finally:
        print('API call finalised.')
   