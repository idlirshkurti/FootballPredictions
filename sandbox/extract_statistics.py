#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 19:37:16 2018
@author: idlirshkurti
"""

import os
import re
import tqdm
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs4


full_stats = []

seasons_full = ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017']

for season in seasons_full:
    print('--------------------------------' + season + '--------------------------------')
    season_stats = []
    path = '/Users/idlirshkurti/Desktop/FootballPredictions/example_html/Eredivisie_' + season +'/'
    files = os.listdir(path)
    files_txt = [i for i in files if i.endswith('statistieken.html')]
    for match in files_txt:
        file = open('./example_html/Eredivisie_' + season +'/' + match)
        soup = bs4(file, "html5lib")
            
        titles = soup.findAll("div", {"class" : 'statText statText--titleValue'})
        columns_main = []
        
        for i in tqdm.tqdm(range(0,len(titles))):
            new = titles[i].contents
            columns_main.append(new)
            
        for x in columns_main: 
            # check if exists in unique_list or not 
            if x not in season_stats:
                season_stats.append(x)
    for w in season_stats:
        if w not in full_stats:
            full_stats.append(w)

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
  
AllColumns.append('Match_ID')
# Create empty data frame
df_full = pd.DataFrame(columns = np.unique(AllColumns))

df_full.loc[0,:] = None





for season in seasons_full:
    print('--------------------------------' + season + '--------------------------------')
    season_stats = []
    path = '/Users/idlirshkurti/Desktop/FootballPredictions/example_html/Eredivisie_' + season +'/'
    files = os.listdir(path)
    files_txt = [i for i in files if i.endswith('statistieken.html')]
    
    df_full = pd.DataFrame(columns = np.unique(AllColumns))
    df_full.loc[0,:] = None

    for j in tqdm.tqdm(range(len(files_txt))):
        
        match = files_txt[j]
        file = open('./example_html/Eredivisie_' + season +'/' + match)
        soup = bs4(file, "html5lib")
        Title = soup.title.contents[0]
        Title = Title.split("|")[0]
        Title = Title.strip()
        Title = Title.split(" ")
        HomeTeam = Title[0]
        AwayTeam = Title[2]  
        DateTime = soup.find_all("div", {"class" : "info-time mstat-date"})[0].contents[0]
        DateTime = DateTime.replace(".", "_")
        DateTime = DateTime.replace(" ", "_")  
    
        
        df_full.loc[j, 'Match_ID'] = HomeTeam + "_" + AwayTeam + "_" + DateTime
        
        overall_stats = soup.findAll("div", {"id" : 'tab-statistics-0-statistic'})[0]
        home_titles = overall_stats.find_all("div", {"class" : 'statText statText--titleValue'})
        away_titles = overall_stats.find_all("div", {"class" : 'statText statText--titleValue'})
        
        for i in range(0,len(home_titles)):
            home_titles[i] = home_titles[i].contents
            
        for i in range(0,len(away_titles)):
            away_titles[i] = away_titles[i].contents 
        
        home_stats = []
        for i in range(0,len(home_titles)):
            home_stats_new = overall_stats.find_all("div", {"class" : 'statText statText--homeValue'})[i].contents
            home_stats.append(home_stats_new)
            
        away_stats = []
        for i in range(0,len(away_titles)):
            away_stats_new = overall_stats.find_all("div", {"class" : 'statText statText--awayValue'})[i].contents
            away_stats.append(away_stats_new)
            
        home = ['Home_']
        away = ['Away_']
        home_titles = [home + cols for cols in home_titles]
        away_titles = [away + cols for cols in away_titles]
        
        home_titles_new = []
        for i in range(0,len(home_titles)):
                new = "".join(home_titles[i])
                home_titles_new.append(new)
        
        away_titles_new = []
        for i in range(0,len(away_titles)):
                new = "".join(away_titles[i])
                away_titles_new.append(new)
                
        away_titles_new = [w.replace(' ', '_') for w in away_titles_new]
        home_titles_new = [w.replace(' ', '_') for w in home_titles_new]
        
        home_titles = home_titles_new
        away_titles = away_titles_new
        
        del home_titles_new, away_titles_new
            
        all_titles = []
        for i in range(0,len(away_titles)):
            new_home = home_titles[i]
            all_titles.append(new_home)
            new_away = away_titles[i]
            all_titles.append(new_away)
          
        all_stats = []
        for i in range(0,len(home_stats)):
            new_home = home_stats[i]
            all_stats.append(new_home)
            new_away = away_stats[i]
            all_stats.append(new_away)
        
        
        
        #df = pd.DataFrame(columns = all_titles)
        #df.loc[0,:] = all_stats
        
        
        for i in range(len(all_stats)):
            df_full.loc[j, all_titles[i]] = int(re.search(r'\d+', all_stats[i][0]).group())
        
        
        
        df_full.to_csv('./data/html_output/full_statistics_' + season + '.csv')
        
df = pd.DataFrame(columns = np.unique(AllColumns))
for season in seasons_full:
    df_new = pd.read_csv('./data/html_output/full_statistics_' + season + '.csv')     
    df = df.append(df_new)
    

df.to_csv('./data/html_output/complete_statistics.csv')



