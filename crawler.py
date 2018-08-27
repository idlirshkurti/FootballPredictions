# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Beautiful soup as html parser
from bs4 import BeautifulSoup as bs4
# Requests to get HTML source code
import requests
# Selenium (with PhantomJS installed seperately) get HTML as in browser
from selenium import webdriver
# Regular expressions
import re
# Pandas
import pandas as pd
# Time for sleep and current time
import time
# Random so they don't see us
from random import random


# Use Selenium and PhantomJS to get usable HTML code (after JS)
browser = webdriver.Chrome("C:/Users/Diederik/Downloads/chromedriver_win32/chromedriver.exe")

def getSource(url):
    # Point Selenium browser to URL and get page source code
    browser.get(url)
    
    # Wait 2-8 seconds for the browser to load content
    time.sleep(random()*6+2)
    
    # Now get the source
    return browser.page_source

# Return the soup (DOM object) to use the document structure
def makeSoup(html):
    # Make the soup
    #soup = bs4(html, 'html.parser') # Built-in Python parser
    soup = bs4(html, 'html5lib')     # HTML5 parser
    return soup

html = makeSoup(getSource("https://google.com"))