# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 17:29:07 2018

@author: Diederik


HTML parser for football data from flashscore.nl

"""


from bs4 import BeautifulSoup as bs4
import pandas as pd
import re
import time
import random
import os
import datetime

# Creating an empty dataframe
df = pd.DataFrame(columns=["DateTime", "Season", "PlayingRound", "HomeTeam", "AwayTeam", "HomeScore", "AwayScore", "HomeHalfTimeScore", "AwayHalfTimeScore", "HomeSecondHalfScore", "AwaySecondHalfScore", "Spectators"])
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['PlayingRound'] = pd.to_numeric(df['PlayingRound'])
df['HomeScore'] = pd.to_numeric(df['HomeScore'])
df['AwayScore'] = pd.to_numeric(df['AwayScore'])
df['HomeHalfTimeScore'] = pd.to_numeric(df['HomeHalfTimeScore'])
df['HomeSecondHalfScore'] = pd.to_numeric(df['HomeSecondHalfScore'])
df['AwaySecondHalfScore'] = pd.to_numeric(df['AwaySecondHalfScore'])
df['Spectators'] = pd.to_numeric(df['Spectators'])


path = 'C:/Users/862371/Desktop/FootballPredictions-master/data/Eredivisie_2016-2017'

# Looking for only the matches with 'samenvatting' in it
x = 1

for i in os.listdir(path):
    if 'samenvatting' in i:
        print (path + i)
        file = path + "/" + i
        print (x)
        x = x + 1

        # file = "C:/Users/Diederik/Desktop/gitrepo_fb_preds/Eredivisie_2016-2017/GRO_EXC_samenvatting-wedstrijd.html"
        File = open(file, "r")   
        Soup = bs4(File, 'html5lib')
        
        
        # Parsing for the speelronde (playing round) of the match
        Reduced = Soup.find_all("div", {"class" : "fleft"})
        PlayingRound = str(Reduced[0].contents[3]).split("-")[1].split("<")[0].strip().split(" ")[1]
        PlayingRound = int(PlayingRound)
        
        
        # Parsing for the datetime of the match
        DateTime = Soup.find_all("div", {"class" : "info-time mstat-date"})[0].contents[0]
        DateTime = DateTime.replace(".", "_")
        DateTime = DateTime.replace(" ", "_")
        
        
        # Parsing for the season of the match
        DateTimeObject = datetime.datetime.strptime(DateTime, "%d-%m-%Y %H:%M")
        Month = DateTimeObject.strftime("%m")
        Year = int(DateTimeObject.strftime("%Y"))
        
        if Month in ["07", "08", "09", "10", "11", "12"] and PlayingRound < 25:
            Season = str(Year) + "-" + str(Year+1)
        else:
            Season = str(Year-1) + "-" + str(Year)
        
        
        # Parsing the title for Teamnames and Score
        Title = Soup.title.contents[0]
        Title = Title.split("|")[0]
        Title = Title.strip()
        Title = Title.split(" ")
        
        HomeTeam = Title[0]
        AwayTeam = Title[2]
        
        Score = Title[1]
        HomeScore = Score.split("-")[0]
        AwayScore = Score.split("-")[1]
        
        
        # Parsing the half time score and second half score
        HomeHalfTimeScore = Soup.find_all("span", {"class" : "p1_home"})[0].contents[0].split("\\")[0]
        AwayHalfTimeScore = Soup.find_all("span", {"class" : "p1_away"})[0].contents[0].split("\\")[0]
        
        HomeSecondHalfScore = Soup.find_all("span", {"class" : "p2_home"})[0].contents[0].split("\\")[0]
        AwaySecondHalfScore = Soup.find_all("span", {"class" : "p2_away"})[0].contents[0].split("\\")[0]
        
        
        # Parsing the number of spectators
        ReducedSpec = Soup.find("table", {"class" : "parts match-information"})
        ReducedSpec = ReducedSpec.find_all("tr", {"class" : "content"})
        
        if len(ReducedSpec) == 2:
            ReducedSpec = ReducedSpec[1].td.contents[0].split("\\")
        elif len(ReducedSpec) == 1:
            ReducedSpec = ReducedSpec[0].td.contents[0].split("\\")
        else:
            ReducedSpec = "ERROR CHECK SCRIPT"
            print ("error in Spectators")
            
        
        search = "Toeschouwers"
        
        for item in ReducedSpec:
            if search in item:
                Spectators = item
                
        Spectators = re.sub(r'\D', '', Spectators)
        
        # Parsing the referee
                
            
            
       
        
        
        
        # Add all variables to the dataframe
        NewInput = pd.DataFrame({'DateTime' : pd.to_datetime(DateTime), 'Season' : [Season], 'PlayingRound' : pd.to_numeric(PlayingRound), 'HomeTeam' : [HomeTeam], 'AwayTeam' : [AwayTeam], 'HomeScore' : pd.to_numeric(HomeScore), 'AwayScore' : pd.to_numeric(AwayScore), 'HomeHalfTimeScore' : pd.to_numeric(HomeHalfTimeScore), 'AwayHalfTimeScore' : pd.to_numeric(AwayHalfTimeScore), 'HomeSecondHalfScore' : pd.to_numeric(HomeSecondHalfScore), 'AwaySecondHalfScore' : pd.to_numeric(AwaySecondHalfScore), 'Spectators' : pd.to_numeric(Spectators)           })
        df = df.append(NewInput)



# Print all to CSV
df.to_csv("C:/Users/862371/Desktop/FootballPredictions-master/output/test.csv", index=False, encoding="utf8", sep=";")