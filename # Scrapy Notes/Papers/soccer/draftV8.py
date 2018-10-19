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
url_2018 = 'http://www.sodasoccer.com/dasai/league/348.html'
res_2018 = requests.get(url_2018,headers = header)
res_2018.encoding = 'utf-8'
tree_2018 = etree.HTML(res_2018.text)
team_2018 = tree_2018.xpath('//div[@class="l_j"]/table[1]//tr/td/a/text()')
ref_2018 = tree_2018.xpath('//div[@class="l_j"]/table[1]//tr/td/a/@href')
url_test = 'http://www.sodasoccer.com'+ref_2018[0]
res_test = requests.get(url_test)
res_test.encoding = 'utf-8'
tree_test = etree.HTML(res_test.text)
tree_test.xpath('//div[@class="listtabel"]/table//tr')
for tr in tree_test.xpath('//div[@class="listtabel"]/table//tr')[1:]:
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
    print(id, name, eng, position, birthday, nation, height, weight, plays, score)

