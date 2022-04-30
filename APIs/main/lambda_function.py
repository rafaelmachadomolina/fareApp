#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:34:20 2022

@author: rafaelmachado
"""

### Import modules
import os
import json
import urllib3
from datetime import datetime

### Constants
TODAY = datetime.now()
DAYS_YEAR = 365.25
PIPELINE_FEAT_ORDER = ['accommodates', 'bedrooms', 'ocupation', 'proximity_score',
                       'seniority', 'bathroom_number', 'min_nights',
                       'total_amenities', 'host_total_listings', 'room_type']

LOG_VARS = ['min_nights', 'total_amenities', 'host_total_listings']

TABLE_SCHEMA = ['accommodates', 'bedrooms', 'ocupation_days', 'ocupation',
                'postcode', 'proximity_score', 'seniority', 'bathroom_number',
                'min_nights', 'total_amenities', 'host_total_listings',
                'room_type', 'predicted_fare', 'customer_name', 'ref_date']

NUM_TYPES = {'accommodates': 'int',
            'bedrooms': 'int',
            'ocupation_days': 'int',
            'seniority': 'int',
            'bathroom_number': 'float',
            'min_nights': 'int',
            'total_amenities': 'int',
            'host_total_listings': 'int'}

### Environment vars
API_PROX_SCORE = os.environ['API_PROX_SCORE']
API_PREPROCESS = os.environ['API_PREPROCESS']
API_PREDICT = os.environ['API_PREDICT']
API_INSERT_DB = os.environ['API_INSERT_DB']

### Process functions

# Parse datatypes
def parse_datatypes(listing_dict, num_types = NUM_TYPES):

    for i in num_types.keys():
        if(num_types[i] == 'int'):
            listing_dict[i] = int(listing_dict[i])
        elif(num_types[i] == 'float'):
            listing_dict[i] = float(listing_dict[i])

    return listing_dict;

# Calculate ocupation
def calculate_ocupation(listing_dict, days_per_year = DAYS_YEAR):
    '''
    '''
    if listing_dict['ocupation_days'] > days_per_year:
        raise Exception('Ocupation nights per year should be less than {:.0f}'.format(days_per_year))

    listing_dict['ocupation'] = listing_dict['ocupation_days'] / days_per_year

    return listing_dict;

def correct_logvars(listing_dict, log_vars = LOG_VARS):

    for i in log_vars:
        listing_dict[i] += 0.1

    return listing_dict;

# Call APIs
def callAPI(apiURL, requestBody):

    httpHandler = urllib3.PoolManager()

    response = httpHandler.urlopen('POST', url = apiURL, body = requestBody)

    if response.status != 200:
        raise Exception('Oh oh. Something went wrong calling an API')

    dataResponse = response.data.decode()
    dataResponse = json.loads(dataResponse) # Eliminates first quotation marks
    dataResponse = json.loads(dataResponse)

    if(dataResponse['statusCode'] != 200):
        raise Exception('The API executed correctly, but response content is not as expected')

    return dataResponse;

# Get proximity score
def get_proximityScore(listing_dict, apiURL = API_PROX_SCORE):
    postcode = listing_dict['postcode']
    body = json.dumps({'postcode': postcode})

    response = callAPI(API_PROX_SCORE, body)

    proximityScore = response['body']['proximity_score']
    listing_dict['proximity_score'] = proximityScore

    return listing_dict;

# Preprocess data
def preprocess_data(listing_dict, apiURL = API_PREPROCESS, feat_order = PIPELINE_FEAT_ORDER):

    listing_dict = correct_logvars(listing_dict)
    request = [listing_dict[i] for i in feat_order]

    body = json.dumps({'record': request})

    response = callAPI(apiURL, body)

    return response['body'];

def predict_fare(p_data, apiURL = API_PREDICT):

    body = json.dumps({'features': p_data})

    response = callAPI(apiURL, body)

    return response['body'];

def insert_to_db(listing, predicted_value, current_date = TODAY, schema = TABLE_SCHEMA, apiURL = API_INSERT_DB):

    listing['predicted_fare'] = predicted_value
    listing['ref_date'] = str(current_date)

    schema_records = {i: listing[j] for i, j in enumerate(schema)}

    body =json.dumps({'record': schema_records, 'schema': schema})

    callAPI(apiURL, body)

### Main execution function
def lambda_handler(event, context):

    try:
        # Load record
        # listing = json.loads(event)
        listing = event
        print('Event read')

        # Parse data
        listing = parse_datatypes(listing)
        print('Data parsed')

        # Compute ocupation rate
        listing = calculate_ocupation(listing)
        print('Ocupation computed')

        # Get proximity score
        listing = get_proximityScore(listing)
        print('Obtained proximity score')

        # Preprocess data
        preprocess_vars = preprocess_data(listing)
        print('Data preprocessed')

        # Predict fare
        predicted_value = predict_fare(preprocess_vars)
        print(f'Value predicted at £{predicted_value}')

        # Save results in table
        insert_to_db(listing, predicted_value)
        print('Data recorded in db')

        # Return value
        response = {"statusCode": 200,
                    "body": predicted_value}
        print('Response generated')

        return json.dumps(response);

    except Exception as e:
        print('Exception', e)

        response = {"statusCode": 400}

        return json.dumps(response);

    finally:
        print('Process finished.')
