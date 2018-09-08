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
from tqdm import tqdm

#os.chdir('repository_path')
from src.DataLoading import *

# Load names of teams

# Variables
url = "https://www.futhead.com/18/leagues/eredivisie/"

# Use Selenium to get python browser
browser = webdriver.Chrome('/Users/idlirshkurti/Downloads/chromedriver')


# Run this to fetch the HTML (as soup object) of the requested page
html = makeSoup(getSource(url))


mydivs = html.findAll("li", {"class": "list-group-item list-group-item-link"})

teams = []

for team in range(0, len(mydivs)):
    team_1 = mydivs[team].find('a').contents[2]
    team_1 = team_1[team_1.find("'")+2:team_1.find("\n")]
    teams.append(team_1)


# Variables
col_names =  ['Team', 'Rating']
team_ratings = pd.DataFrame(columns = col_names)

browser = webdriver.Chrome('/Users/idlirshkurti/Downloads/chromedriver')

for tm in tqdm(range(0, len(teams))): # ~4min to run
    time.sleep(random()*6+2)
    team = teams[tm]
    team1 = team.replace(" ", "-")
    url = "https://www.futhead.com/18/clubs/"+team1+"/"

    # Run this to fetch the HTML (as soup object) of the requested page
    html = makeSoup(getSource(url))

    mydivs = html.findAll("div", {"class": "display-inline-block hvr-grow"})
    player_rating = html.findAll("div", {"class" : 'playercard-rating'})

    ratings = []
    for player in range(0, len(player_rating)):
        ratings.append(int(get_price(player_rating[player])))
    
    # average rating of the team            
    av_rating = np.mean(ratings)
    # append into dataframe
    new_input = pd.DataFrame({'Team': [team], 'Rating': av_rating})
    team_ratings = team_ratings.append(new_input)
    

team_ratings.to_pickle("./team_ratings.pkl")
