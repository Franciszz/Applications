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