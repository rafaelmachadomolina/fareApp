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
TABLE_NAME = 'model.predictions'

def insert_data(conn, record, schema):
    
    fields = tuple(record[str(i)] for i in range(len(record)))
    columns = str(tuple(schema))
    columns = columns.replace("'", "")
    
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {TABLE_NAME}{columns} VALUES {str(fields)}")
    cur.close()

    

# def lambda_handler(event, context):
def lambda_handler(event, context):
    
    response = {}
    
    # Get postcode from event
    record = event['record']
    schema = event['schema']
    
    try:
        connection = psycopg2.connect(host=DB_HOST,
                                      port=DB_PORT,
                                      dbname=DB_NAME,
                                      user=DB_USERNAME,
                                      password=DB_PASSWORD)

        insert_data(connection, record, schema)

        connection.commit()
        connection.close()

        response = {"statusCode": 200,
                    "body": "Successful insert."}
        
        return json.dumps(response)
        
    except:
        print('Oh oh, something went wrong with the call')
        
        response = {"statusCode": 400,
                    "body": ""}
        
        return json.dumps(response)
        
    finally:
        print('API call finalised.')