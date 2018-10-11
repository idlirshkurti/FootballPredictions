#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 19:37:16 2018

@author: idlirshkurti
"""

import os
import re
import tqdm
import time
import requests
import numpy as np
import pandas as pd
from random import random
from selenium import webdriver
from bs4 import BeautifulSoup as bs4


# Variables
season = "2016-2017"
url = "https://www.voetbaluitslagen.nl/eredivisie-"+season+"/uitslagen/"
targetFolder = "/Users/idlirshkurti/Desktop/FootballPredictions/data/"


# Use Selenium to get python browser
browser = webdriver.Chrome('/Users/idlirshkurti/Downloads/chromedriver')

# Run this to fetch the HTML (as soup object) of the requested page
html = makeSoup(getSource(url))

# All the files ending with 'statistieken.html'
path = '/Users/idlirshkurti/Desktop/FootballPredictions/example_html/Eredivisie_2016-2017/'
files = os.listdir(path)
files_txt = [i for i in files if i.endswith('statistieken.html')]

full_stats = []

for match in files_txt:

    file = open('./example_html/Eredivisie_2016-2017/' + match)
    soup = bs4(file, "html5lib")
        
    titles = soup.findAll("div", {"class" : 'statText statText--titleValue'})
    columns_main = []
    
    for i in tqdm.tqdm(range(0,len(titles))):
        new = titles[i].contents
        columns_main.append(new)
        
    for x in columns_main: 
        # check if exists in unique_list or not 
        if x not in full_stats:
            full_stats.append(x)

statistics = pd.DataFrame(columns = full_stats)
home = ['Home_']
away = ['Away_']
HomeCols = [home + cols for cols in columns_main]
AwayCols = [away + cols for cols in columns_main]

HomeColumns = []
for i in tqdm.tqdm(range(0,len(HomeCols))):
        new = "".join(HomeCols[i])
        HomeColumns.append(new)

AwayColumns = []
for i in tqdm.tqdm(range(0,len(AwayCols))):
        new = "".join(AwayCols[i])
        AwayColumns.append(new)
        
AwayColumns = [w.replace(' ', '_') for w in AwayColumns]
HomeColumns = [w.replace(' ', '_') for w in HomeColumns]

AllColumns = []
for i in tqdm.tqdm(range(0,len(AwayCols))):
    new_home = HomeColumns[i]
    AllColumns.append(new_home)
    new_away = AwayColumns[i]
    AllColumns.append(new_away)
  

# Create empty data frame
df_full = pd.DataFrame(columns = np.unique(AllColumns))

df_full.loc[0,:] = None









for j in tqdm.tqdm(range(len(files_txt))):
    match = files_txt[j]

    file = open('./example_html/Eredivisie_2016-2017/' + match)
    soup = bs4(file, "html5lib")
    
    overall_stats = soup.findAll("div", {"id" : 'tab-statistics-0-statistic'})[0]
    home_titles = overall_stats.find_all("div", {"class" : 'statText statText--titleValue'})
    away_titles = overall_stats.find_all("div", {"class" : 'statText statText--titleValue'})
    
    for i in tqdm.tqdm(range(0,len(home_titles))):
        home_titles[i] = home_titles[i].contents
        
    for i in tqdm.tqdm(range(0,len(away_titles))):
        away_titles[i] = away_titles[i].contents 
    
    home_stats = []
    for i in tqdm.tqdm(range(0,len(home_titles))):
        home_stats_new = overall_stats.find_all("div", {"class" : 'statText statText--homeValue'})[i].contents
        home_stats.append(home_stats_new)
        
    away_stats = []
    for i in tqdm.tqdm(range(0,len(away_titles))):
        away_stats_new = overall_stats.find_all("div", {"class" : 'statText statText--awayValue'})[i].contents
        away_stats.append(away_stats_new)
        
    home = ['Home_']
    away = ['Away_']
    home_titles = [home + cols for cols in home_titles]
    away_titles = [away + cols for cols in away_titles]
    
    home_titles_new = []
    for i in tqdm.tqdm(range(0,len(home_titles))):
            new = "".join(home_titles[i])
            home_titles_new.append(new)
    
    away_titles_new = []
    for i in tqdm.tqdm(range(0,len(away_titles))):
            new = "".join(away_titles[i])
            away_titles_new.append(new)
            
    away_titles_new = [w.replace(' ', '_') for w in away_titles_new]
    home_titles_new = [w.replace(' ', '_') for w in home_titles_new]
    
    home_titles = home_titles_new
    away_titles = away_titles_new
    
    del home_titles_new, away_titles_new
        
    all_titles = []
    for i in tqdm.tqdm(range(0,len(away_titles))):
        new_home = home_titles[i]
        all_titles.append(new_home)
        new_away = away_titles[i]
        all_titles.append(new_away)
      
    all_stats = []
    for i in tqdm.tqdm(range(0,len(home_stats))):
        new_home = home_stats[i]
        all_stats.append(new_home)
        new_away = away_stats[i]
        all_stats.append(new_away)
    
    
    
    #df = pd.DataFrame(columns = all_titles)
    #df.loc[0,:] = all_stats
    
    
    for i in range(len(all_stats)):
        df_full.loc[j, all_titles[i]] = all_stats[i]



