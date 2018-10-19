import requests
import random
import time
from bs4 import BeautifulSoup
import lxml
from lxml import etree
# ===================================================================================
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url = 'http://csldata.sports.sohu.com/team.php?season=2004&type=P'
# =========  中超 ==============================================================================================
zc_list = []
for year in range(2004,2019):
    print(year)
    url = 'http://csldata.sports.sohu.com/'+'team.php?season={}&type=P'.format(year)
    print(url)
    res = requests.get(url, headers = myheader)
    res.encoding = 'utf-8'
    time.sleep(random.randint(1,2))
    soup = BeautifulSoup(res.content,'html.parser')
    srcs = soup.find('ul',{'class': 'roll680_team'}).findAll('li')
    for src in srcs:
        teamname = src.get_text()
        teamsrc = src.find('a').get('href')
        url_team =  'http://csldata.sports.sohu.com/'+ teamsrc
        res_team = requests.get(url_team, headers = myheader)
        res_team.encoding = 'utf-8'
        time.sleep(random.randint(1,3))
        tree = lxml.etree.HTML(res_team.content)
        tab = tree.xpath('//div[@id="content1_1"]/table')[0]
        for tr in tab[0].xpath('//tr')[1:]:
            te = tr.xpath('td/text()')
            tname = tr.xpath('td/a/text()')
            te = te + tname
            ln = len(te)
            while (len(te) < 9) & (len(te) > 0):
                te = te + tname
            te = te + [ln, year, teamname]
            zc_list.append(te)


len(zc_list)
import pandas as pd
import copy
zc_ll = copy.deepcopy(zc_list)
zc_df = pd.DataFrame(zc_list)
zc_df.to_excel('zc_sohu.xlsx')








