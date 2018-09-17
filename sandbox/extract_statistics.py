#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 19:37:16 2018

@author: idlirshkurti
"""

from bs4 import BeautifulSoup as bs4
import requests
from selenium import webdriver
import re
import pandas as pd
import time
from random import random
import numpy as np
import tqdm


file = open('./example_html/ADO_GRO_wedstrijdstatistieken.html')
soup = bs4(file, "html5lib")

df = pd.DataFrame(columns = [''])

titles = soup.findAll("div", {"class" : 'statText statText--titleValue'})
columns_main = []

for i in tqdm.tqdm(range(0,len(titles))):
    new = titles[i].contents
    columns_main.append(new)

HomeTeam = soup.findAll("div", {"class" : 'tname__text'})[0].contents[3].contents
AwayTeam = soup.findAll("div", {"class" : 'tname__text'})[1].contents[1].contents

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
    
df = pd.DataFrame(columns = AllColumns)

soup.findAll("div", {"class" : 'statText statText--homeValue'})

HomeStats = []
for i in tqdm.tqdm(range(0,len(HomeColumns))):
    new = soup.findAll("div", {"class" : 'statText statText--homeValue'})[i].contents
    HomeStats.append(new)
    
AwayStats = []
for i in tqdm.tqdm(range(0,len(HomeColumns))):
    new = soup.findAll("div", {"class" : 'statText statText--awayValue'})[i].contents
    AwayStats.append(new)

AllStats = []
for i in tqdm.tqdm(range(0,len(AwayCols))):
    new_home = HomeStats[i]
    AllStats.append(new_home)
    new_away = AwayStats[i]
    AllStats.append(new_away)
    
df_new = pd.DataFrame([AllStats], columns = AllColumns)

df = df.append(df_new)



