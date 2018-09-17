# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
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
season = "2016-2017"
url = "https://www.voetbaluitslagen.nl/eredivisie-"+season+"/uitslagen/"
targetFolder = "C:/Users/Diederik/Desktop/gitrepo_fb_preds/Eredivisie_2016-2017/"




# Use Selenium to get python browser
browser = webdriver.Chrome("C:/Users/Diederik/Downloads/chromedriver_win32/chromedriver.exe")


# Run this to fetch the HTML (as soup object) of the requested page
html = makeSoup(getSource(url))



# Click on load more games to get the full page
while not html.select_one('table#tournament-page-results-more')['style'] == 'display: none;':
    # Click on the loadMoreGames() anchor
    print('Clicking on loadMoreGames()')
    browser.find_element_by_css_selector('table#tournament-page-results-more').click()
                                         
    
    # Wait some time for the browser to load the content
    time.sleep(random()*6+2)

    # Make another soup and repeat
    html = makeSoup(browser.page_source)






#open file with *.html* extension to write html
file = open("C:/Users/Diederik/Desktop/gitrepo_fb_preds/"+season+".html","w")

#write then close file
file.write(str(html))
file.close()





# Out of the HTML fetch the ID's of all regular season games (starting with 'g_1_') and put them in a list:

# First filter out 'nacompetitie' and playoffs'
if season == "2017-2018":
    eredivisieId = "l_1_4K9Dfl6U"    # Season 17/18
elif season == "2016-2017":
    eredivisieId = "l_1_Uuh1RiXn"    # Season 16/17
elif season == '2015-2016':
    eredivisieId = "l_1_6Ty1wfGO"    # Season 15/16
elif season == '2014-2015':
    eredivisieId = "l_1_zahr8PMr"    # Season 14/15
elif season == '2013-2014':
    eredivisieId = "l_1_z7xQ7ZEj"    # Season 13/14
elif season == '2012-2013':
    eredivisieId = "l_1_lbWpn3AO"    # Season 12/13

# Find the tablerows with the right eredivisieId
leagueRows = html.select("tr.league." + eredivisieId)

# Find the parent table and combine them in a string
combinedTables = ""
for row in leagueRows:
    # Get parent table and append
    combinedTables += str(row.find_parent('table', class_='soccer'))

# Turn the string back into Soup object
html_reduced = makeSoup(combinedTables)

# Then find all indentifiers (table rows with id starting with g_1_)
identifiers = []
for row in html_reduced.find_all('tr', id=re.compile('^g_1_')):
    # Now trim (remove 'g_1_') and put it in our list
    identifiers.append(row['id'][4:])


# Should be 306 matches in a season
print('Number of matches found: ' + str(len(identifiers)))


# Now all the identifiers are known, it can crawl through all matches and save them as html in a folder

# Store the source codes in...
print('Storing files in folder: ' + targetFolder)

# All match statistics consist of three tabs
tabs = ["samenvatting-wedstrijd", "wedstrijdstatistieken", "opstellingen"]

for idx in identifiers:

    for tab in tabs:
        # Get the exact gameUrl by putting the identifier in place and the tab
        gameUrl = getGameUrl(idx, tab)
        # Make a soub object of the page
        soup = makeSoup(getSource(gameUrl))
