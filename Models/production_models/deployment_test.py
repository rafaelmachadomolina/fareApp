#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 23:44:52 2022

@author: rafaelmachado
"""

import pickle

def pl_add(x):
    return x + 0.1;

def pl_add_inv(x):
    return x - 0.1;

with open('./pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

with open('./predictive_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
X = [[5, 1, 0.5, 0.6, 8, 1.5, 2, 10, 2, 'Private room'],
     [2, 1, 0.5, 0.6, 8, 1.5, 2, 10, 2, 'Private room']]
    
X_t = pipeline.transform(X)

y = model.predict(X_t)