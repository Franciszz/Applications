# ===========================================================================================
# 球员数据
# ===========================================================================================
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
url = 'http://data.champdas.com/person/rank-1-2014.html'
res = requests.get(url,headers=myheader)
res.encoding = 'utf-8'
rep = res.text
soup = BeautifulSoup(rep,'html.parser')
tables = soup.find_all('table')
tt_list = []
for tb in soup.find_all('table'):
    for tbody in tb.find_all('tbody'):
        print(tbody.get(''))
for tb in soup.find_all('table'):
    for tbody in tb.find_all('tbody'):
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                tt = td.getText()
                tt_list.append(tt)
tt_list
print(tt_list)

tab1 = tables[1]
tab2 = tables[2]
tab3 = tables[3]
import lxml
from lxml import etree

# ============================================================
# =============== test
# ============================================================

url = 'http://data.champdas.com/person/rank/attack.html'
form_data = {
    'leagueId':1,
    'season':2014,
    'orderType':6,
    'offset':2,
    'totalSize':286,
    'personType':2,
    'dataType':2
}
res0 = requests.session()
res = res0.post(url,headers=myheader,data=form_data)
res.status_code
print(res.text)
# ============================================================
# =============== selenium
# ============================================================
from scrapy.http import HtmlResponse, Request
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# chrome_options.binary_location = '/opt/google/chrome/chrome'
opener = webdriver.Chrome(chrome_options=chrome_options)
opener.implicitly_wait(10)
# opener.maximize_window()
url = 'http://data.champdas.com/person/rank-1-2017.html'
opener.get(url)

opener.find_element_by_xpath('//div[@id="tab1"]/div[@class="menu"]/ul/li[@id="one2"]').click()
opener.get_screenshot_as_file('test.png')
html = opener.page_source
opener.execute_script()
print(html)
res = BeautifulSoup(html,'lxml')
res.title
res.body.find_all(class="content")
body = res.find_all('body')
content = body.find_all('div[@class="content"]')