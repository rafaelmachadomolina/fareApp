#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 21:19:36 2022

@author: rafaelmachado
"""

### Import packages
import os
import json
import psycopg2

### Define env variables
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

### Define constants
TABLE_NAME = 'model.proximity_score'
SELECT_COLS = 'postcode, score_stations'

def get_data_SQL(conn, postcode):
    
    try:
        
        cur = conn.cursor()
        cur.execute(f"SELECT {SELECT_COLS} FROM {TABLE_NAME} WHERE postcode = '{postcode}' LIMIT 1")
        rows = cur.fetchall()
        cur.close()
        
        if(len(rows) == 0):
            raise Exception('Postcode not found')
        
        proximity_score = float(rows[0][1])
        
        return proximity_score;
        
    except:
        
        errorMessage = f'Could not retrieve any results for postcode {postcode}'
        print(errorMessage)
        raise Exception(errorMessage)
    

# def lambda_handler(event, context):
def handler(event, context):
    
    response = {}
    
    # Get postcode from event
    postcode = event['postcode']
    
    try:
        connection = psycopg2.connect(host = DB_HOST,
                                port = DB_PORT,
                                dbname = DB_NAME,
                                user = DB_USERNAME,
                                password = DB_PASSWORD)
        
        proximity_score = get_data_SQL(connection, postcode)
        
        connection.close()
        
        response = {"statusCode": 200,
                    "body": {"postcode": postcode,
                             "proximity_score": proximity_score}}
        
        return json.dumps(response)
        
    except:
        print('Oh oh, something went wrong with the call')
        
        response = {"statusCode": 400,
                    "body": ""}
        
        return json.dumps(response)
        
    finally:
        print('API call finalised.')