#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 18:59:08 2018

@author: idlirshkurti
"""

from bs4 import BeautifulSoup as bs4
import requests
from selenium import webdriver
import re
import pandas as pd
import time
from random import random
import os

#os.chdir('repository_path')
from src.DataLoading import *

# Variables
team = "ajax"
url = "https://www.futhead.com/18/clubs/"+team+"/"

# Use Selenium to get python browser
browser = webdriver.Chrome('/Users/idlirshkurti/Downloads/chromedriver')


# Run this to fetch the HTML (as soup object) of the requested page
html = makeSoup(getSource(url))

mydivs = html.findAll("div", {"class": "display-inline-block hvr-grow"})
player_rating = html.findAll("div", {"class" : 'playercard-rating'})

ratings = []
for player in range(0, len(player_rating)-1):
    ratings.append(int(get_price(player_rating[player])))
                
np.mean(ratings)
        
        



