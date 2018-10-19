# ==============================================================================
# ====================获取球员名单
# ==============================================================================
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import random
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
def get_url(url):
    res = requests.get(url, headers = myheader)
    res.encoding = 'utf8'
    tree = etree.HTML(res.text)
    urls = tree.xpath('//div[@class="mw-category-group"]//li/a/@href')
    return urls
url1 = 'http://wiki.cfadata.com/index.php?title=%E5%88%86%E7%B1%BB:%E7%90%83%E5%91%98'
url_1 = get_url(url1)
url2 = 'http://wiki.cfadata.com/index.php?title=%E5%88%86%E7%B1%BB:%E7%90%83%E5%91%98&pagefrom=Tan%2CJun+Jin%0A%E9%99%88%E4%BF%8A%E4%BB%81#mw-pages'
url_2 = get_url(url2)
url_all = ['http://wiki.cfadata.com'+ url for url in url_1+url_2]
len(url_all)
# ==============================================================================
# ==================== 获取球员信息
# ==============================================================================
inf_base = []
i = 0
for url in url_all:
    res_i = requests.get(url, headers = myheader)
    res_i.encoding = 'utf-8'
    tree = etree.HTML(res_i.text)
    tables = tree.xpath('//table[@class="wikitable"]')[0]
    for tr in tables.xpath('//tr')[2:14]:
        inf = tr.xpath('td/text()')
        inf_base.append(inf)
    time.sleep(random.choice(range(6)))
    i += 1
    print('第【{}】个球员成功'.format(i))
plyinf = dict(
    name = [],
    nameen = [],
    nation = [],
    place = [],
    birth = [],
    position = [],
    weight = [],
    height = []
)
import re
inf_base
inf_base2 = [''.join(inf).strip('\n') for inf in inf_base]
for i in range(288):
    plyinf['name'].append(inf_base2[12*i+0])
    plyinf['nameen'].append(inf_base2[12 * i + 1])
    plyinf['birth'].append(inf_base2[12 * i + 4])
    plyinf['position'].append(inf_base2[12 * i + 10])
    plyinf['height'].append(inf_base2[12 * i + 8])
    plyinf['weight'].append(inf_base2[12 * i + 9])
    plyinf['nation'].append(inf_base2[12 * i + 7])
    plyinf['place'].append(inf_base2[12 * i + 6])
import pandas as pd

#plyinf['birth']=[birth[:-5] for birth in plyinf['birth']]
plyinf_df = pd.DataFrame(plyinf)
plyinf_df.to_csv('ply_inf.csv',encoding='utf-8')
plyinf_df_raw = pd.DataFrame(inf_base2)
plyinf_df_raw.to_csv('ply_inf_raw.csv',encoding='utf-8')