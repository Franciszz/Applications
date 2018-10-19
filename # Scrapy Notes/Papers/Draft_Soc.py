import pandas as pd
import re

info_ply = pd.read_excel('info_ply_1.xlsx',na_values='')
# ====== 身高
pat_h = re.compile(r'(\d{1}\.?\d{2})厘?米')
def cat_height(x, pat=pat_h):
    if x:
        x = str(x).replace('cm','厘米')
        x = str(pat.findall(x)).replace('.','')
    else:
        x = None
    return x[1:-1]
info_ply['身高'] = info_ply['身高'].apply(cat_height)
# ======= 出场和得分
score_list = []
play_list = []
for x in info_ply.iloc[:,-1]:
    if x:
        x = str(x)
        xlist = x.split(',')
        if len(xlist)>1:
            score_list.append(xlist[-1])
            play_list.append(xlist[-2])
        else:
            score_list.append(xlist[0])
            play_list.append('nan')
    else:
        score_list.append('nan')
        play_list.append('nan')
info_ply['score'] = score_list
info_ply['play'] = play_list
def cat_pos(x):
    x = str(x)
    if x:
        if x.startswith(''):
            x = x[1:]
    return x
info_ply['位置'] = info_ply['位置'].apply(cat_pos)
info_ply.to_excel('info_ply_3.xlsx')
# ======================== 国足出场统计
adult = pd.read_excel('SoccerSample005.xlsx', sheet_name='国青出场统计')
adult['info'] = adult['info'].apply(lambda x: x[:-1])
adult['date'] = adult['info'].str.split("'.'", expand=True)[0]
adult['place'] = adult['info'].str.split("'.'", expand=True)[1]
adult['game'] = adult['info'].str.split("'.'", expand=True)[2]
adult['opponent'] = adult['info'].str.split("'.'", expand=True)[3]
adult['score'] = adult['info'].str.split("'.'", expand=True)[4]
def pre_player(x):
    x_list = x.split('：')
    if len(x_list)>=2:
        plypos = x_list[0]
        plyname = x_list[1]
    else:
        plypos = None
        plyname = x_list[-1]
    return plypos, plyname
ply1, ply2 = [], []
adult['player'] = adult['player'].apply(lambda x: x[2:-2]).str.replace("'",'')
for x in adult.player:
    pl1,pl2 = pre_player(x)
    ply1.append(pl1)
    ply2.append(pl2)
adult['player'] = ply2
adult.player = adult['player'].str.replace('[)）.\d+]','')
adult.player = adult['player'].str.replace(' ','')
adult.player = adult['player'].str.replace('[（(、，]',',')
adult.player = adult['player'].str.replace('S','')
adult.to_excel('adult.xlsx')
adult['player'] = adult.player.str.strip()
def player_count(df):
    plylist = []
    for plyls in df.player:
        plylist += plyls.split(',')
    return plylist
# adult.year.drop_duplicates()
player_dict = {
    'year':[],
    'player':[]
}
for year in range(2000,2019):
    namelist = player_count(adult.loc[adult['year']==year,:])
    print(len(namelist))
    yearlist = [year]*len(namelist)
    player_dict['year'] += yearlist
    player_dict['player'] += namelist
player_df = pd.DataFrame(player_dict)
player_df.to_excel('adult.xlsx')
player_df_count = pd.DataFrame(player_df.groupby(['year','player']).size())
player_df_count.to_excel('adult_count.xlsx')
# ======================== 国足出场统计
 teen = pd.read_excel('SoccerSample005.xlsx', sheet_name='国青出场统计')
# date_list = []
# place_list = []
# game_list = []
# opponent_list = []
# score_list = []
# for x in teen['info']:
#     date, place, game, opponent, score = x.split("','")
#     date_list.append(date)
#     place_list.append(place)
#     game_list.append(game)
#     opponent_list.append(opponent)
#     score_list.append(score)
# teen['date'] = teen['info'].str.split("','", expand=True)[0]
# teen['place'] = teen['info'].str.split("','", expand=True)[1]
# teen['game'] = teen['info'].str.split("','", expand=True)[2]
# teen['opponent'] = teen['info'].str.split("','", expand=True)[3]
# teen['score'] = teen['info'].str.split("','", expand=True)[4]
def pre_player(x):
    x_list = x.split('：')
    if len(x_list)>=2:
        plypos = x_list[0]
        plyname = x_list[1]
    else:
        plypos = None
        plyname = x_list[-1]
    return plypos, plyname
ply1, ply2 = [], []
teen['player'] = teen['player'].apply(lambda x: x[2:-2]).str.replace("'",'')
for x in teen.player:
    pl1,pl2 = pre_player(x)
    ply1.append(pl1)
    ply2.append(pl2)
teen['player'] = ply2
teen.player = teen['player'].str.replace('[)）.\d+]','')
teen.player = teen['player'].str.replace(' ','')
teen.player = teen['player'].str.replace('[（(、，]',',')
teen.player = teen['player'].str.replace(",,,",',')
teen.to_excel('teen.xlsx')
teen['player'] = teen.player.str.strip()
def player_count(df):
    plylist = []
    for plyls in df.player:
        if plyls:
            plylist += plyls.split(',')
    return plylist
# teen.year.drop_duplicates()
player_dict_teen = {
    'year':[],
    'player':[],
    'type':[]
}
teen.to_excel('teen.xlsx')
teen.player = teen.player.fillna('nan')
for year_index in range(2000,2019):
    for type_index in teen.loc[teen['year']==year_index,'type'].drop_duplicates():
        print(year_index ,type_index)
        namelist = player_count(teen.loc[(teen['year']==year_index)&(teen['type']==type_index),:])
        yearlist = [year_index] * len(namelist)
        typelist = [type_index] * len(namelist)
        player_dict_teen['year'] += yearlist
        player_dict_teen['player'] += namelist
        player_dict_teen['type'] += typelist
        print(len(namelist))
len(player_dict_teen['year'])

player_df_teen = pd.DataFrame(player_dict_teen)
player_df.to_excel('teen_list.xlsx')
player_df_teen_count = pd.DataFrame(player_df_teen.groupby(['year','type','player']).size())
player_df_teen_count.to_excel('teen_count.xlsx')


from urllib.request import urlopen
from io import StringIO
import csv
data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv")\
    .read().decode('ascii', 'ignore')
data
'%s.png'% str(data)
dataFile = StringIO(data)
dataFile
csvReader = csv.reader(dataFile)
for row in csvReader:
    print(row)

import numpy as np
lol = pd.read_excel('lol.xlsx',sheet_name='Sheet1')
lol.redBans = lol.redBans.str.strip('[').str.replace("'",'').str.strip(' ')
Champ_list = [Champ.strip(' ') for Champ in Champ_list]
dummies = pd.DataFrame(np.zeros((len(lol),len(Champ_list))),columns=Champ_list)
dummies.shape
for i, Champ in enumerate(lol.redBans):
    Champ = str(Champ)
    for ban in Champ.split(', '):
        dummies.loc[i, ban] = 1
dummies.shape
Champ_list



import sys
import pdfminer
import importlib

