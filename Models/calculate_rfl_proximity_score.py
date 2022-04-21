#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:42:30 2022

@author: rafaelmachado
"""

import os
import boto3
import pandas as pd
from haversine import haversine

### Define environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
S3_PARQUET_BUCKET_NAME = os.environ.get('AWS_BUCKET_PARQUET')

### Initialise parameters
s3_client = boto3.client("s3")
DB_URL = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
PARQUET_PATH = './SchemaReadyData_parquet/'

### Define functions
def transport_score(df_points, target_lat, target_lon, calibration):

    target_tuple = (target_lat, target_lon)
    latitude_list = df_points['latitude'].tolist()
    longitude_list = df_points['longitude'].tolist()

    source_tuples = [(i, j) for i, j in zip(latitude_list, longitude_list)]
    distance_list = [haversine(i, target_tuple) for i in source_tuples]
    df_points['distance'] = distance_list
    df_points['score_mark'] = df_points['distance'] <= calibration

    score = sum(df_points['score_mark']) / len(df_points['score_mark'])
    return score;

### Bring postcodes
try:

    df_stations = pd.read_sql_table('tfl_stations', DB_URL, schema = 'city')
    df_postcodes = pd.read_sql_table('postcodes', DB_URL, schema = 'city')

    print('Table retrieved successfully.')
except:
    print('Oh oh, something happened mate. Try again.')
    
### Score each postcode
df_postcodes_merged = df_postcodes.copy()

listings_lat = df_postcodes_merged['latitude']
listings_lon = df_postcodes_merged['longitude']

score_stations = [transport_score(df_stations,
                                  listings_lat[j],
                                  listings_lon[j],
                                  10) for j in range(len(listings_lat))]

df_postcodes_merged['score_stations'] = score_stations

### Filter columns
COLS = ['id', 'postcode', 'neighbourhood_id', 'postcode_url', 'score_stations', 'active']

df_postcodes_out = df_postcodes_merged[COLS]

### Export to SQL table
try:
    df_postcodes_out.to_sql('proximity_score',
                            DB_URL,
                            schema = 'model',
                            if_exists = 'append',
                            index = False,
                            method = 'multi')
    
    print('Successfully inserted rows into target table')
except:
    print('Oh oh, something happened mate inserting rows. Try again.')

### Save backup locally and S3 dedicated buquet
df_postcodes_out.to_parquet(PARQUET_PATH + 'proximity_score.parquet', index = False)

files = [f for f in os.listdir(PARQUET_PATH) if os.path.isfile(os.path.join(PARQUET_PATH, f))]
for f in files:
    s3_client.upload_file(PARQUET_PATH + f, S3_PARQUET_BUCKET_NAME, f)
