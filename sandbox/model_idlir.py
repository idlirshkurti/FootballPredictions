#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 20:13:47 2018

@author: idlirshkurti
"""

import pandas as pd
import numpy as np

dta_location = os.path.join("..","data/2008_2009")
data_file = "N1.csv"


import os

data_frames = []

for root, dirs, files in os.walk(data_location):
    if data_file in files:
        data_frames.append(pd.read_csv(os.path.join(root,data_file)))
        
data = pd.concat(data_frames)


print(len(data))
data.columns.values

data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%y')
all_data = data.set_index('Date')

data = all_data[['HomeTeam', 'AwayTeam']] 
data.head(5)

g = input_features.columns.to_series().groupby(data.dtypes).groups

object_features = {key.name: value for key, value in g.items()}['object']

# Define baseline model

bins = np.bincount(output)
index = np.nonzero(bins)[0]
np.vstack((index,bins[index])).T

# Validation

def report_scoring(scores):
    print("List of scores: " + str(scores))
    print("mean scoring: " + str(scores.mean()))
    print("Standard deviation between scorings: " + str(scores.std()))

from sklearn.model_selection import cross_val_score

scores = cross_val_score(**THE MODEL**, **INPUT FEATURES**, **SUPERVISED OUTCOME**)

report_scoring(scores)

# Example
trained_random_forest_model = random_forest_model.fit(input_features,output)
pd.Series(trained_random_forest_model.feature_importances_, input_features.columns)


