# ====================================================================
# 俱乐部历史战绩
# ====================================================================
import requests
import time
from bs4 import BeautifulSoup
import random
import socket
import http.client
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
def get_content(url):
    header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    while True:
        try:
            res = requests.get(url, headers = header)
            res.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))
        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))
    return res.text
club_hist = {
        'rank':[], 'div':[], 'codeid':[], 'club':[],
        'team':[], 'english':[], 'plays':[], 'points':[],
        'wins':[], 'draws':[], 'loss':[], 'gscores':[],
        'gagainst':[], 'netscore':[], 'year':[]
    }
for i in range(2018,2019):
    url = 'http://www.cfadata.com/cfa-{}.php'.format(i)
    print('Crawl page:', url)
    html_text = get_content(url)
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.findAll('table')[0]
    for tr in table.find_all('tr')[3:-3]:
        club_hist['rank'].append(tr.find_all('td')[0].getText())
        club_hist['div'].append(tr.find_all('td')[1].getText())
        club_hist['codeid'].append(tr.find_all('td')[2].getText())
        club_hist['club'].append(tr.find_all('td')[3].getText())
        club_hist['team'].append(tr.find_all('td')[4].getText())
        club_hist['english'].append(tr.find_all('td')[5].getText())
        club_hist['plays'].append(tr.find_all('td')[6].getText())
        club_hist['points'].append(tr.find_all('td')[7].getText())
        club_hist['wins'].append(tr.find_all('td')[8].getText())
        club_hist['draws'].append(tr.find_all('td')[9].getText())
        club_hist['loss'].append(tr.find_all('td')[10].getText())
        club_hist['gscores'].append(tr.find_all('td')[11].getText())
        club_hist['gagainst'].append(tr.find_all('td')[12].getText())
        club_hist['netscore'].append(tr.find_all('td')[13].getText())
        club_hist['year'].append(i)
import pandas as pd
club_hist_df = pd.DataFrame(club_hist)
club_hist_df.to_csv('club_hist2018.csv',encoding='utf8')








