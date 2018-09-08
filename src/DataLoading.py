#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:18:56 2018

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


# Go to the URL
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


def getGameUrl(identifier, page):
    gameUrl = 'https://www.voetbaluitslagen.nl/wedstrijd/id/#page'
    return url.replace('id', identifier).replace('page', page)

def get_price(tr):
    for integer in tr:
        return(integer)

