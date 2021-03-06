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
import random
import os

# Seasons to scrape:
seasons = ["2016-2017"]

for season in seasons:

    
    print ("Starting Season "+season)
    
    # Variables
    url = "https://www.flashscore.nl/eredivisie-"+season+"/uitslagen/"
    targetFolder = "C:/Users/Diederik/Desktop/gitrepo_fb_preds/Eredivisie_"+season+"/"
    
    # Create targetfolder if not exists
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    
    
    
    
    # Use Selenium to get python browser
    #browser = webdriver.Chrome("C:/Users/Diederik/Downloads/chromedriver_win32/chromedriver.exe")
    
    
    # Go to the URL
    def getSource(url):
        # Point Selenium browser to URL and get page source code
        browser.get(url)
        
        # Wait 2-8 seconds for the browser to load content
        sleepTime = random.randrange(4, 8) - random.random()
    
        time.sleep(sleepTime)
        
        # Now get the source
        return browser.page_source
    
    
    
    
    # Return the soup (DOM object) to use the document structure
    def makeSoup(html):
        # Make the soup
        #soup = bs4(html, 'html.parser') # Built-in Python parser
        soup = bs4(html, 'html5lib')     # HTML5 parser
        return soup
    
    
    
    def getGameUrl(identifier, page):
        url = 'https://www.flashscore.nl/wedstrijd/id/#page'
        return url.replace('id', identifier).replace('page', page)
    
    
    # Run this to fetch the HTML (as soup object) of the requested page
    html = makeSoup(getSource(url))
    
    
    
    # Click on load more games to get the full page
    while not html.select_one('table#tournament-page-results-more')['style'] == 'display: none;':
        # Click on the loadMoreGames() anchor
        print('Clicking on loadMoreGames()')
        browser.find_element_by_css_selector('table#tournament-page-results-more').click()
                                             
        
        # Wait some time for the browser to load the content
        time.sleep(random.randrange(4, 7))
    
        # Make another soup and repeat
        html = makeSoup(browser.page_source)
    
    
    
    
    
    
    #open file with *.html* extension to write html
    file = open("C:/Users/Diederik/Desktop/gitrepo_fb_preds/"+season+".html","w")
    
    #encode html to utf8
    html_tofile = html.encode("utf8")
    
    #write then close file
    file.write(str(html_tofile))
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
    
    i = 1
    
    for idx in identifiers:
    
        for tab in tabs:
            # Get the exact gameUrl by putting the identifier in place and the tab
            gameUrl = getGameUrl(idx, tab)
            
            #Make a soub object of the page
            soup = makeSoup(getSource(gameUrl))       
            
    
            # Write the html to a file
            # Create name of the file
            match = str(soup.title)[7:18]
            match = match[0:3] + "_" + match[-3:]
            filename = match + "_" + tab + ".html"
            
            #open file to write html
            file = open(targetFolder + filename ,"w")
            
            #encoding to utf8
            soup = soup.encode("utf8")
            
            #write then close file
            file.write(str(soup))
            file.close()
        
            
            
        print('Running: ' + str(i) + ' | ' + idx)
        i += 1
    
    
    
