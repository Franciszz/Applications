# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 11:17:22 2017

@author: Franc
"""
# =============================================================================
# 深圳二手房
# =============================================================================
import requests
url = 'http://sz.centanet.com/ershoufang/'
response = requests.get(url)
response.encoding
response.apparent_encoding
ttt = response.text

##解析网页
from chardet import detect
res = response.content
cder = detect(res)
res = res.decode(cder.get('encoding'))
import lxml.html
from lxml import etree
res2 = response.text
tree = etree.HTML(res)
###获取小区名称
dist_name = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-name"]/a/@title')
###获取小区地址
dist_region = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-txt"][2]/span/text()')
###获取楼层建筑
room_build = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-txt"][1]/span[1]/text()')
###获取房间朝向
room_direction = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-txt"][1]/span[2]/text()')
###获取房间装修类型
room_deco_type = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-txt"][1]/span[3]/text()')
###获取房间建造年份
room_year = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-txt"][1]/span[4]/text()')
###获取房间总价
room_price_t = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-pricearea fr"]/p[@class="price-nub cRed tc"]/span/text()')
###获取房间均价
room_price = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-pricearea fr"]/p[@class="price-txt tc"]/text()')
###获取所在小区均价
room_price_dist = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-pricearea fr"]/p[@class="price-txtB tc"]/text()')
###获取房间链接
room_link = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/h4[@class="house-title"]/a/@href')
###房间其他信息
room_inf_ect = tree.xpath('//div[@class="house-item clearfix"]/div[@class="item-info fl"]/p[@class="house-name"]/span/text()')

# =============================================================================
# Python+Selenium 爬取实习僧招聘网爬虫
# =============================================================================
import os
import random
import time
# ============================================================
# =============== overall
# ============================================================
def getlaogou(driver,url):
    #初始化一个长度为0的空字典！以备之后收集数据
    myresult = {
              "position_name":[],
              "position_company":[],
              "position_salary":[],
              "position_link":[],
              "position_exprience":[],
              "position_industry":[],
              "position_environment":[]
              }
    #导航到目标网址
    driver.get(url)
    #计时器初始化
    i =0
    while True:
        #计时器累计计时：
        i+=1
        #获取当前页面DOM
        pagecontent = driver.page_source
        #解析HTML文档
        result = etree.HTML(pagecontent)
        #使用字典内单个list的extend方法累计收集数据
        myresult["position_name"].extend(result.xpath('//ul[@class="item_con_list"]/li/@data-positionname'))
        myresult["position_company"].extend(result.xpath('//ul[@class="item_con_list"]/li/@data-company'))
        myresult["position_salary"].extend(result.xpath('//ul[@class="item_con_list"]/li/@data-salary'))
        myresult["position_link"].extend(result.xpath('//div[@class="p_top"]/a/@href'))
        myresult["position_exprience"].extend([ text.xpath('string(.)').strip() for text in  result.xpath('//div[@class="p_bot"]/div[@class="li_b_l"]')])
        myresult["position_industry"].extend([ text.strip() for text in  result.xpath('//div[@class="industry"]/text()')])
        myresult["position_environment"].extend(result.xpath('//div[@class="li_b_r"]/text()'))
        #单次循环任务休眠
        time.sleep(random.choice(range(3)))
        #判断页面是否到尾部
        if result.xpath('//div[@class="page-number"]/span[1]/text()')[0] != '30':
            #如果未到达页面尾部，则点击下一页：
            driver.find_element_by_xpath('//div[@class="pager_container"]/a[last()]').click()
            #同时打印当前任务 状态！
            print("第【{}】页抓取成功!".format(i))
        else:
            #如果所有页面到达尾部，则跳出循环！
            break
    #打印全局任务状态
    print("everything is OK")
    #退出并关闭selenium服务！
    driver.quit()
    #返回数据
    return pd.DataFrame(myresult)
url = "https://www.lagou.com/zhaopin"
mydata = getlaogou(driver,url)
print(mydata)
# =============================================================================
# requests：用来抓取网页的html源代码 
# csv：将数据写入到csv文件中 
# random：取随机数 
# time：时间相关操作 
# socket和http.client 在这里只用于异常处理 
# BeautifulSoup：用来代替正则式取源码中相应标签中的内容 
# urllib.request：另一种抓取网页的html源代码的方法，但是没requests方便（我一开始用的是这一种）
# =============================================================================
# =============================================================================
# 爬取苏州最近七天天气
# =============================================================================
import requests
import csv
import random 
import time
import socket
import http.client
from bs4 import BeautifulSoup
# 获取网页源代码
url = 'http://www.weather.com.cn/weather/101190401.shtml '
def get_content(url,data=None):
    #header 是重新用chrome打开网页的第一个请求。
    header ={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
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
    return rep.text
    # return html_text
get_content(url)
# 获取我们所需要的字段最近7天的天气以及最高气温和最低气温
def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text,'html.parser')
    body = bs.body
    data = body.find('div',{'id':'7d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:
        temp = []
        date = day.find('h1').string
        temp.append(date)
        inf = day.find_all('p')
        temp.append(inf[0].string,)
        if inf[1].find('span') is None:
            temperature_highest = None
        else:
            temperature_highest = inf[1].find('span').string
            temperature_highest = temperature_highest.replace('℃','')
        temperature_lowest = inf[1].find('i').string
        temperature_lowest = temperature_lowest.replace('℃', '')
        temp.append(temperature_highest)
        temp.append(temperature_lowest)
        final.append(temp)
    return final
# 保存抓取的文件
def write_data(data,name):
    file_name = name
    with open(file_name,'a',errors= 'ignore',newline = '') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)
if __name__ == '__main__':
    url ='http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'weather.csv')
# =============================================================================
# 模拟登入知乎 
# =============================================================================
# 作者：洛克
# 链接：https://www.zhihu.com/question/48482120/answer/111122902
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
# 
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Date    : 2016-07-14 17:44:54
# 
# import requests
# from pyquery import PyQuery as pq
# import time
# 
# s = requests.session()
# url = "https://www.zhihu.com/#signin"
# login_url = "https://www.zhihu.com/login/email"
# 
# headers = {
#     "Host":"www.zhihu.com",
#     "Referer":"https://www.zhihu.com/",
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
# }
# data = {
#     "email":"xxxx",
#     "password":"xxxxx",
#     "rememberme":"true"
# 
# }
# 
# # 获取 xsrf
# req = s.get(url, headers=headers)
# # print(req)
# doc = pq(req.text)
# xsrf = doc('input[name="_xsrf"]')
# data['_xsrf'] = xsrf
# 
# # 获取 验证码
# # timestamp = int(time.time() * 1000)
# # captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
# # # print captchaURL
# 
# # with open('zhihucaptcha.gif', 'wb') as f:
# #     captchaREQ = s.get(captchaURL)
# #     f.write(captchaREQ.content)
# # loginCaptcha = input('input captcha:\n').strip()
# # data['captcha'] = loginCaptcha
# 
# login = s.post(login_url,  headers=headers, data=data)
# print(login.text)     
# =============================================================================
# =============================================================================
import requests
from bs4 import BeautifulSoup
def login():
    header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    session = requests.session()
    res = session.get('http://www.zhihu.com',headers = header).content
    _xsrf = '66396638636236662d633736612d346435622d383962382d343837623863366165613364'
    login_data = {
            '_xsrf':_xsrf,
            'password':'family404zh',
            'remember_me':'true',
            'email':'1559844145@qq.com'}
    session.post('https://www.zhihu.com/#signin',data=login_data,headers=header)
    res = session.get('http://www.zhihu.com')
    print(res.text)
if __name__=='__main__':
    login()

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
#构造Requests headers
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
headers = {
        'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/',
        'User-Agent':agent}
# 使用cookies
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('Cookie 未加载')
def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'https://www.zhihu.com/'
    #获取登入时需要的_xsrf
    index_page = session.get(index_url,headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
     # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]
# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login(secret, account):
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'phone_num': account
        }
    else:
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'email': account
        }
    # 不需要验证码直接登录成功
    login_page = session.post(post_url, data=postdata, headers=headers)
    login_code = login_page.json()
    if login_code['r'] == 1:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.json()
        print(login_code['msg'])
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()

try:
    input = raw_input
except:
    pass


if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)

# =============================================================================
# 多线程爬虫
# =============================================================================
import time
import threading

def print_nums(s):
    for i in range(5):
        time.sleep(1)
        print('线程',s,':',i)
class MyThread(threading.Thread):
    def __init__(self,s):
        threading.Thread.__init__(self)
        self.s= s
    def run(self):
        print_nums(self.s)
if __name__=="__main":
    thread=[]
    start =time.time()
    for j in range(5):
        t = MyThread(j)
        thread.append(t)
    for t in thread:
        t.start()
    for t in thread:
        t.join()
    end= time.time()
    print('运行时间:',end-start,'s')
# =============================================================================
# 微信公众号爬虫   
# =============================================================================
import wechatsogou
ws_api = wechatsogou.WechatSogouAPI()
ws_api - wechatsogou.WechatSogouAPI(captcha_break_time=3)
ws_api = wechatsogou.WechatSogouAPI(proxies={
        "http": "127.0.0.1:8888",
    "https": "127.0.0.1:8888",})            
      
# =============================================================================
# 今日头条
# =============================================================================
import json
import os
from urllib.parse import urlencode
import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import re
from multiprocessing import Pool
from hashlib import md5
from json.decoder import JSONDecodeError
from config import *
    
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'format': 'json',
        'keyword': keyword,
        'offset': offset,
    }
    params = urlencode(data)
    base = 'http://www.toutiao.com/search_content/'
    url = base + '?' + params
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def parse_page_index(text):
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('title')
    title = result[0].get_text() if result else ''
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Successfully Saved to Mongo', result)
        return True
    return False


def main(offset):
    text = get_page_index(offset, KEYWORD)
    urls = parse_page_index(text)
    for url in urls:
        html = get_page_detail(url)
        result = parse_page_detail(html, url)
        if result: save_to_mongo(result)


pool = Pool()
groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
pool.map(main, groups)
pool.close()
pool.join()

# =============================================================================
# 猫眼电影
# =============================================================================
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    pool.close()
    pool.join()
