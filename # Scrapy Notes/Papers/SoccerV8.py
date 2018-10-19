import requests
import time
import random
import pandas as pd
import numpy as np
from lxml import etree
from bs4 import BeautifulSoup
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
# =========================================================================================
# ====== 中甲球员数据 ======
# =========================================================================================
dict_zj = {
    'id': [], 'name':[], 'eng':[], 'position':[],
    'birthday':[], 'nation':[], 'height':[], 'weight':[],
    'plays':[], 'score':[], 'team':[], 'year':[]
}
for i in range(2008,2019):
    if i < 2018:
        url = 'http://www.sodasoccer.com/dasai/league/%d/348.html' % i
    else:
        url = 'http://www.sodasoccer.com/dasai/league/348.html'
    res = requests.get(url, headers = header)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)
    teams = tree.xpath('//div[@class="l_j"]/table[1]//tr/td/a/text()')
    refs = ['http://www.sodasoccer.com'+ele for ele in tree.xpath('//div[@class="l_j"]/table[1]//tr/td/a/@href')]
    for j in range(len(refs)):
        url_team = refs[j]
        res_team = requests.get(url_team, headers = header)
        time.sleep(random.randint(0,2))
        res_team.encoding = 'utf-8'
        tree_team = etree.HTML(res_team.text)
        tree_team.xpath('//div[@class="listtabel"]/table//tr')
        for tr in tree_team.xpath('//div[@class="listtabel"]/table//tr')[1:]:
            id = tr.xpath('td[1]/text()')
            name = tr.xpath('td[2]/a/text()')
            eng = tr.xpath('td[3]/a/text()')
            position = tr.xpath('td[4]/text()')
            birthday = tr.xpath('td[5]/text()')
            nation = tr.xpath('td[6]/text()')
            height = tr.xpath('td[7]/text()')
            weight = tr.xpath('td[8]/text()')
            plays = tr.xpath('td[9]/text()')
            score = tr.xpath('td[10]/text()')
            print(id, name, eng, position, birthday, nation, height, weight, plays, score, teams[j],i)
            dict_zj['id'].append(id),
            dict_zj['name'].append(name),
            dict_zj['eng'].append(eng),
            dict_zj['position'].append(position),
            dict_zj['birthday'].append(birthday),
            dict_zj['nation'].append(nation),
            dict_zj['height'].append(height),
            dict_zj['weight'].append(weight),
            dict_zj['plays'].append(plays),
            dict_zj['score'].append(score),
            dict_zj['team'].append(teams[j]),
            dict_zj['year'].append(i)
df_zj = pd.DataFrame(dict_zj)
df_zj.to_excel('df_zj.xlsx')
# =========================================================================================
# ====== 中乙球员数据 ======
# =========================================================================================
dict_zy = {
    'id': [], 'name':[], 'eng':[], 'position':[],
    'birthday':[], 'nation':[], 'height':[], 'weight':[],
    'plays':[], 'score':[], 'team':[], 'year':[]
}
url_0 = 'http://www.sodasoccer.com/dasai/league/375.html'
res = requests.get(url_0, headers=header)
res.encoding = 'utf-8'
tree = etree.HTML(res.text)
teams = tree.xpath('//div[@class="l_j"]/table[1]//tr/td/a/text()')
refs = ['http://www.sodasoccer.com' + ele for ele in tree.xpath('//div[@class="l_j"]/table[1]//tr/td/a/@href')]
for i in range(len(refs)):
    url = refs[i]
    res = requests.get(url)
    time.sleep(random.randint(0,2))
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)
    divs = tree.xpath('//div[@class="left"]/div[@id="div4"]/div[@class="listtabel"]/div')[2:]
    print(teams[i],len(divs))
    for j in range(len(divs)):
        div = divs[j]
        trs = div.xpath('table//tr')
        if len(trs) > 1:
            for tr in trs[1:]:
                id = tr.xpath('td[1]/text()')
                name = tr.xpath('td[2]/a/text()')
                eng = tr.xpath('td[3]/a/text()')
                position = tr.xpath('td[4]/text()')
                birthday = tr.xpath('td[5]/text()')
                nation = tr.xpath('td[6]/text()')
                height = tr.xpath('td[7]/text()')
                weight = tr.xpath('td[8]/text()')
                plays = tr.xpath('td[9]/text()')
                score = tr.xpath('td[10]/text()')
                dict_zy['id'].append(id),
                dict_zy['name'].append(name),
                dict_zy['eng'].append(eng),
                dict_zy['position'].append(position),
                dict_zy['birthday'].append(birthday),
                dict_zy['nation'].append(nation),
                dict_zy['height'].append(height),
                dict_zy['weight'].append(weight),
                dict_zy['plays'].append(plays),
                dict_zy['score'].append(score),
                dict_zy['team'].append(teams[i]),
                dict_zy['year'].append(int(2018-j))
                print(int(2018-j),teams[i],name)
df_zy = pd.DataFrame(dict_zy)
df_zy.to_excel('df_zy.xlsx')

# =========================================================================================
# ====== 国青队报名名单 ======
# =========================================================================================
url_teen = 'http://wiki.cfadata.com/index.php?title=%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E7%94%B7%E5%AD%90%E9%9D%92%E5%B0%91%E5%B9%B4%E8%B6%B3%E7%90%83%E9%98%9F%E6%AF%94%E8%B5%9B%EF%BC%881999%EF%BC%89'
res = requests.get(url_teen, headers = header)
res.encoding = 'utf-8'
tree = etree.HTML(res.text)
years = tree.xpath('//td[@class="roundy bl-超级 bw-1 at-l"]/p/a/text()')[-11:]
url_list_teen = ['http://wiki.cfadata.com' + url for url in
                 tree.xpath('//td[@class="roundy bl-超级 bw-1 at-l"]/p/a/@href')[-11:]]
nation_sign = {
    'id':[], 'name':[], 'date':[], 'position':[], 'team':[],
    'year':[], 'level':[], 'game':[]
}
for i in range(len(years)):
    url = url_list_teen[i]
    res = requests.get(url, headers = header)
    time.sleep(random.randint(0,2))
    res.encoding = 'utf-8'
    tree = etree.HTML(res.content)
    tocs = tree.xpath('//div[@id = "toc"]/ul/li')
    for toc in tocs:
        level = toc.xpath('a/span[2]/b/text()')
        game_list = toc.xpath('ul/li/a/span[2]/text()')
        for game in game_list:
            trs = tree.xpath('//h3/span[text()="%s"]/../following-sibling::table[2]//tr'%game)
            for tr in trs[1:]:
                id = tr.xpath('td[1]/text()')
                name = tr.xpath('td[2]/text()')
                date = tr.xpath('td[3]/text()')
                position = tr.xpath('td[4]/text()')
                team = tr.xpath('td[5]/text()')
                nation_sign['id'].append(id)
                nation_sign['name'].append(name)
                nation_sign['date'].append(date)
                nation_sign['position'].append(position)
                nation_sign['team'].append(team)
                nation_sign['year'].append(years[i])
                nation_sign['level'].append(level)
                nation_sign['game'].append(game)
                print(years[i],level, game, name)
df_nas = pd.DataFrame(nation_sign)
df_nas.to_excel('df_nas.xlsx')
# =========================================================================================
# ====== 全运会名单 ======
# =========================================================================================
play_list = pd.read_excel('SoccerSample009.xlsx',sheet_name='Sheet1')
play_list['name'] = play_list.neme.str.replace('\S','')
text = []
for a in play_list.neme:
    tt = pat.findall(a)
    te = ''.join(tt)
    print(te)
    text.append(te)
play_list.neme = text
play_list.to_excel('play_list.xlsx')

play_dict = {
    'province':[],
    'level':[],
    'name':[],
    'birth':[],
    'pos':[],
    'id':[],
    'num':[]
}
for i in range(16):
    plays = play_list.iloc[:,i]
    for j in range(40):
        play_dict['province'].append(plays[0])
        play_dict['level'].append(plays[1])
        play_dict['name'].append(plays[3+j*6])
        play_dict['birth'].append(plays[5+j*6])
        play_dict['id'].append(plays[4+j*6])
        play_dict['pos'].append(plays[6+j*6])
        play_dict['num'].append(plays[2+j*6])
pd.DataFrame(play_dict).to_excel('play_dict1.xlsx')


