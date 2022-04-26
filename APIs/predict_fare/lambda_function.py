#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:48:50 2022

@author: rafaelmachado
"""

### Import modules
import json
import model

### Execute pipeline
def execute_model(model, X):
    y = model.predict(X)
    
    return round(y, 2);

def lambda_handler(event, context):
    
    # Define responses
    response_bad = {"statusCode": 400,
                    "body": None}
    
    # Get data from the event
    X = event['features']
        
    #Execute model
    try:
        body = execute_model(model, X)
        print('Pipeline correctly executed')
        
    except ValueError as e:
        print('Value error:', e)
        return json.dumps(response_bad)
        
    except Exception as e:
        print('Something went wrong with the model execution')
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
   