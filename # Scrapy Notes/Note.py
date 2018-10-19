# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:55:01 2017

@author: Franc
"""

# =============================================================================
# requests让HTTP服务人类http://docs.python-requests.org/zh_CN/latest/
# Requests 允许你发送纯天然，植物饲养的 HTTP/1.1 请求，
# 无需手工劳动。你不需要手动为 URL 添加查询字串，也不需要对 POST 数据进行表单编码。
# Keep-alive 和 HTTP 连接池的功能是 100% 自动化的，
# 一切动力都来自于根植在 Requests 内部的 urllib3。
# =============================================================================

# =============================================================================
# step1 发送请求
# =============================================================================
import requests
r = requests.get('https://github.com/timeline.json')#r是一个response对象
r = requests.post("http://httpbin.org/post")
r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")
# =============================================================================
# step2 传递url参数
# =============================================================================
payload = {'key1':'value1','key2':'value2'}
r = requests.get('http://httpbin.org/get',params=payload)
# =============================================================================
# 通过打印URL，可以看出URL已被正确编码
# 字典中的None的key不会被添加到URL的查询字符串中
# =============================================================================
print(r.url)
payload1 = {'key1':'value1','key2':['value2','value3']}
r = requests.get('http://httpbin.org/get',params=payload1)
print(r.url);print(r.__attrs__)
# =============================================================================
# step3 响应内容，读取服务器的内容
# =============================================================================
import requests
r = requests.get('http://github.com/timeline.json');r.text
# =============================================================================
# 请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。
# 当你访问 r.text 之时，Requests 会使用其推测的文本编码。可以通过r.encoding找出
# 编码，也可通过该函数改变编码r.encoding = 'objective encoding'
# =============================================================================

# =============================================================================
# 二进制相应内容,例如，以请求返回的二进制数据创建一张图片，你可以使用如下代码
# =============================================================================
r.content
import requests
# url = 'https://movie.douban.com/top250'
# r = requests.get(url);r.__attrs__
# r.text()
# r.content
from PIL import Image
from io import BytesIO
i = Image.open(BytesIO(r.content))

# =============================================================================
# json响应内容，内置json解码器处理json数据
# =============================================================================
import requests
r = requests.get('https://github.com/timeline.json')
r.json()
r = requests.get('https://github.com/timeline.json', stream=True)#原始请求
r.raw;r.raw.read(10)

# =============================================================================
# 定制请求头：request header
# 如果你想为请求添加 HTTP 头部，只要简单地传递一个 dict 给 headers 参数就可以了
# 如果在 .netrc 中设置了用户认证信息，使用 headers= 设置的授权就不会生效。而如果设置了 auth= 参数，``.netrc`` 的设置就无效了。
# 如果被重定向到别的主机，授权 header 就会被删除。
# 代理授权 header 会被 URL 中提供的代理身份覆盖掉。
# 在我们能判断内容长度的情况下，header 的 Content-Length 会被改写。
# =============================================================================
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)

# =============================================================================
# POST请求
# =============================================================================
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("http://httpbin.org/post", data=payload)
print(r.text)
payload = (('key1', 'value1'), ('key1', 'value2'))
r = requests.post('http://httpbin.org/post', data=payload)
print(r.text)
# which is equivalent to 
payload = {'key1':['value1','value2']}
r = requests.post('http://httpbin.org/post', data=payload)
print(r.text)
# =============================================================================
# 很多时候你想要发送的数据并非编码为表单形式的。如果你传递一个 string 而不是一个 dict，
# 那么数据会被直接发布出去
# =============================================================================
import json
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
r.text
url = 'https://developer.github.com/v3'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
r.url
r.text
# POST一个多部分编码(Multipart-Encoded)的文件
# 上传多部分编码文件
url = 'http://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)
r.text
# 显式地设置文件名，文件类型和请求头
url = 'http://httpbin.org/post'
files = {'file': ('report.xls', open('report.xls', 'rb'), 
                  'application/vnd.ms-excel', {'Expires': '0'})}
r = requests.post(url, files=files)
r.text
# 发送作为文件来接收的字符串
url = 'http://httpbin.org/post'
files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
r = requests.post(url, files=files)
r.text

# =============================================================================
# 响应状态码和响应状态码
# =============================================================================
r = requests.get('http://httpbin.org/get')
r.status_code
r.status_code == requests.codes.ok
r.raise_for_status()
bad_r = requests.get('http://httpbin.org/status/404')
bad_r.status_code#错误的请求
bad_r.raise_for_status()
r.headers['Content-Type']
r.__attrs__
r.__doc__
r.headers.get('content-type')
# =============================================================================
# cookies以及发送cookies参数
# =============================================================================
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
r.text
r.cookies['example_cookie_name']
url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
r.text
# cookies的返回对象
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
url = 'http://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
r.text
# =============================================================================
# 重定向和请求历史
# =============================================================================
r = requests.get('http://github.com')
r.url
r.status_code
r.history
# 若使用了HEAD
r = requests.head('http://github.com', allow_redirects=True)
r.url

# =============================================================================
# 超时反应设置告诉 requests 在经过以 timeout 参数设定的秒数时间之后停止等待响应。
# 基本上所有的生产代码都应该使用这一参数。如果不使用，你的程序可能会永远失去响应
# =============================================================================
requests.get('http://github.com', timeout=0.001)

# =============================================================================
# 高级用法
# =============================================================================

# =============================================================================
# 会话对象：会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有
# 请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能。所以如果你向
# 同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
# =============================================================================
s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
print(r.text)
# 提供缺省数据
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})
# both 'x-test' and 'x-test2' are sent
s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
s = requests.Session()
r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)
r = s.get('http://httpbin.org/cookies')
print(r.text)
# =============================================================================
# 如果你要手动为会话添加 cookie，就使用 Cookie utility 函数 来操纵 Session.cookies。
# 会话还可以用作前后文管理器
# =============================================================================
with requests.Session() as s:
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# =============================================================================
# 请求与响应对象
# =============================================================================
r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
r.headers
r2 = requests.get('http://movie.douban.com/top250')
r2.headers
r2._content
r2.request.headers
# =============================================================================
# 准备的请求当你从 API 或者会话调用中收到一个 Response 对象时，
# request 属性其实是使用了 PreparedRequest.有时在发送请求之前，
# 你需要对 body 或者 header （或者别的什么东西）做一些额外处理
# =============================================================================
from requests import Request,Session
s = Session()
req = Request('GET',url,data=data,headers=header)
prepped = req.prepare()
resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)
print(resp.status_code)
# =============================================================================
# SSL证书验证
# =============================================================================
requests.get('https://requestb.in')#未设置证书
requests.get('https://github.com', verify=True)
requests.get('https://github.com', verify='/path/to/certfile')
# requests.get(url,verify='pathtocertedfile')
s = requests.Session();s.verify = '/path/to/certfile'
# =============================================================================
# 客户端证书（可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组）
# =============================================================================
requests.get('https://kennethreitz.org', 
             cert=('/path/client.cert', '/path/client.key'))
s = requests.Session()
s.cert = '/path/client.cert'
# =============================================================================
# 自定义身份验证自定义的身份验证机制是作为 requests.auth.AuthBase 的子类来实现的，
# 在 requests.auth 中提供身份验证方案： HTTPBasicAuth 和 HTTPDigestAuth 
# =============================================================================
from requests.auth import AuthBase
class PizzaAuth(AuthBase):
    def __init__(self,username):
        self.username = username
    def __call__(self,r):
        r.headers['X-Pizza'] = self.username
        return r
requests.get('http://pizzabin.org/admin', auth=PizzaAuth('kenneth'))
# =============================================================================
# 代理
# =============================================================================
import requests
proxies = {
        'http':'http://10.10.1.10:3128',
        'https':'http://10.10.1.10:1080'}
requests.get('http://example.org',proxies=proxies)
# HTTP动词
import requests
r = requests.get('https://api.github.com/repos/requests/requests/git/commits/a050faf084662f3a352dd1a941f2c7c9f886d4ad')
if(r.status_code==requests.codes.ok):
    print(r.headers['Content-Type'])
commit_data = r.json()
print(commit_data.keys())
commit_data[u'committer']
commit_data[u'tree']
verbs = requests.options(r.url);verbs.status_code
verbs = requests.options('http://a-good-website.com/api/cats')
r = requests.get('https://api.github.com/requests/kennethreitz/requests/issues/482')
r.status_code
issue = json.loads(r.text)
print(issue[u'title'])
print(issue[u'comments'])
# 有 3 个评论。我们来看一下最后一个评论。
r = requests.get(r.url + u'/comments')
r.status_code
comments = r.json()
print comments[0].keys()
print comments[2][u'body']
print comments[2][u'user'][u'login']
body = json.dumps({u"body": u"Sounds great! I'll get right on it!"})
url = u"https://api.github.com/repos/requests/requests/issues/482/comments"
r = requests.post(url=url, data=body)
r.status_code
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('fake@example.com', 'not_a_real_password')
r = requests.post(url=url, data=body, auth=auth)
r.status_code
content = r.json()
print(content[u'body'])
print(content[u"id"])
body = json.dumps({u"body": u"Sounds great! I'll get right on it once I feed my cat."})
url = u"https://api.github.com/repos/requests/requests/issues/comments/5804413"
r = requests.patch(url=url, data=body, auth=auth)
r.status_code
r = requests.delete(url=url, auth=auth)
r.status_code
r.headers['status']
r = requests.head(url=url, auth=auth)
print r.headers

# =============================================================================
# 基本身份认证
# =============================================================================
from requests.auth import HTTPBasicAuth
r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
r1 = requests.get('https://l.xmu.edu.cn/my/')
r1.url#failed
r2 = requests.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1010%26response_type%3Dcode',
                  auth=HTTPBasicAuth('15420171151976', 'family404xmu'))
r2.content#failed
from requests.auth import HTTPDigestAuth
r3 = requests.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1010%26response_type%3Dcode',
                  auth=HTTPDigestAuth('15420171151976', 'family404xmu'))
r3.status_code
r3.url#failed
# =============================================================================
# netrc 认证.如果认证方法没有收到 auth参数，Requests将试图从用户的 netrc文件中获取 
# URL 的 hostname 需要的认证身份。
# The netrc file overrides raw HTTP authentication headers set with headers=.
# =============================================================================
# 摘要式身份认证
from requests.auth import HTTPDigestAuth
url = 'http://httpbin.org/digest-auth/auth/user/pass'
requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
# =============================================================================
# scrapy
# =============================================================================
import scrapy
class QuoteSpider(scrapy.Spider):
    name ='quotes'
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

# =============================================================================
# Requests and Beautifulsoup
# =============================================================================
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import urllib
import urllib
# make a request
r = requests.get('http://mt.sohu.com/20161016/n470376857.shtml')
print(len(r.content))
print(len(r.text));print(r.encoding)
# parse JSON
location='厦门大学'
url_1 = 'http://apis.map.qq.com/ws/geocoder/v1/?address='
url_2 = urllib.urlencode(location)
url_3 = '&key='
url_4 = 'MH3BZ-4CF36-XKDSV-MYRUU-A5U6T-2HFKG'
url = ''.join(url_1,url_2,url_3,url_4)
print url
import requests
r = requests.get('h
                 ttp://github.com/timeline.json')
import matplotlib as mp
mpl.
print(r.content)

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc)
print(soup)
soup.title
soup.title.name
soup.title.string
soup.title.parent.name
soup.p
soup.head
soup.p['class']
soup.a
soup.find_all('p')
soup.find_all('a')
soup.find(id='link3')
for link in soup.find_all('a'):
    print(link.get('href'))
from bs4 import BeautifulSoup 
soup.a.string#character
soup.a.contents#list
print(soup.a.prettify())
soup.contents
