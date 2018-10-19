# -*- coding: utf-8 -*-

#==========================================
# 豆瓣登录
#==========================================
import requests
import re
### 构造请求头
from faker import Factory
### 登录的网址
url_login = 'https://accounts.douban.com/login'
### 登录信息
formdata = {
    'source': 'index_nav',
    'form_email': '1559844145@qq.com',
    'form_password' : 'family404db',
    'captcha-solution': 'thunder',
    'captcha-id':'Fb8uBgENlo8hP4iUyZnGS0r2:en'
}
f = Factory.create()
headers= {'User-Agent': f.user_agent()}
res0 = requests.session()
res1 = res0.post(url_login,headers=headers, data=formdata)
res1.status_code
res1.content.decode('utf8')
#==========================================
# 京东登录
#==========================================
from bs4 import BeautifulSoup
import time
class JD_crawl:
    def __init__(self, username, password):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'https://www.jd.com/',
        }
        self.login_url = 'https://passport.jd.com/new/login.aspx'
        self.post_url = 'https://passport.jd.com/uc/loginService'
        self.auth_url = 'https://password.jd.com/uc/showAuthCode'
        self.session = requests.session()
        self.username = '15059336436'
        self.password = 'family404jd'
    def get_login_info(self):
        html = self.session.get(self.login_url, headers = self.headers).content
        soup = BeautifulSoup(html, 'lxml')
        uuid = soup.select('#uuid')[0].get('value')
        eid = soup.select('#eid')[0].get('value')
        fp = soup.select('input[name="fp"]')[0].get('value')
        _t = soup.select('input[name="_t"]')[0].get('value')
        login_type = soup.select('input[name="loginType"]')[0].get('value')
        pub_key = soup.select('input[name="pubKey"]')[0].get('value')
        sa_token = soup.select('input[name="sa_token"]')[0].get('value')

        auth_page = self.session.post(self.auth_url, data={'loginName':self.username}).text
        if 'true' in auth_page:
            auth_code_url = soup.select('#JD_Verification1')[0].get('src2')
            auth_code = str(self.get_auth_img(auth_code_url))
        else:
            auth_code = ''
        data = {
            'uuid': uuid,
            'eid': eid,
            'fp': fp,
            '_t': _t,
            'loginType': login_type,
            'loginname': self.username,
            'nloginpwd': self.password,
            'chkRememberMe': True,
            'pubKey': pub_key,
            'sa_token': sa_token,
            'authcode': auth_code
        }
        return data
    def get_auth_img(self, url):
        auth_code_url = 'http:{}&yys={}'.format(url, str(int(time.time()*1000)))
        auth_img = self.session.get(auth_code_url, headers=self.headers)
        with open('auth.img', 'wb') as f:
            f.write(auth_img.content)
        code_typein = input('请输入验证码: ')
        return code_typein
    def login(self):
        data = self.get_login_info()
        headers = {
            'Referer': self.post_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            login_page = self.session.post(self.post_url, data=data, headers=headers)
            print('Success!',login_page.text())
        except Exception as e:
            print('Error e')
    def shopping(self):
        carshop = self.session.post('https://cart.jd.com/cart.action', headers=self.headers)
        print(carshop.encoding)

if __name__ == '__main__':
    un = input('请输入京东账号：')
    pwd = input('请输入京东密码：')
    jd = JD_crawl(un, pwd)
    jd.login()
    jd.shopping()

#==========================================
# 豆瓣登录:POST登录
#==========================================
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove

class DB_crawl:
    def __init__(self, username, password):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'https://www.douban.com/'
        }
        self.login_url = 'https://accounts.douban.com/login'
        self.datas['form_email'] = username
        self.datas['form_pwd'] = password
        self.session = requests.session()
    def get_auth_img(self):
        auth_page = self.session.post(self.login_url,headers=self.headers,
                                      data=self.datas).content
        soup = BeautifulSoup(auth_page, 'lxml')
        img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
        urlretrieve(img_src, 'captcha.jpg')
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print('到本地目录打开captcha.jpg获取验证码')
        finally:
            captcha = input('请输入验证码: ')
            remove('captcha.jpg')
        captcha_id = soup.find(
            'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
        return captcha, captcha_id
    def isLogin():
        # 通过查看用户个人账户信息来判断是否已经登录
        url = "https://www.douban.com/accounts/"
        login_code = session.get(url, headers=headers,
                                 allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False
    def login(self):
        captcha, captcha_id = get_auth_img()
        # 增加表数据
        self.datas['captcha-solution'] = captcha
        self.datas['captcha-id'] = captcha_id
        login_page = session.post(url, data=datas, headers=headers).content
        soup = BeautifulSoup(login_page, "html.parser")
        result = soup.findAll('div', attrs={'class': 'title'})
        for item in result:
            print(item.find('a').get_text())
if __name__ == '__main__':
    if isLogin():
        print('Login successfully')
    else:
        login()
#==========================================
# 豆瓣登录:cookies登录
#==========================================
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
try:
    import cookielib
except:
    import http.cookiejar as cookielib
try:
    from PIL import Image
except:
    pass
url = 'https://accounts.douban.com/login'
datas = {'source': 'index_nav',
         'remember': 'on'}
headers = {'Host':'www.douban.com',
           'Referer': 'https://www.douban.com/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate, br'}
# 尝试使用cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookies未能加载")
    #cookies加载不成功，则输入账号密码信息
    datas['form_email'] = input('Please input your account:')
    datas['form_password'] = input('Please input your password:')
def get_captcha():
    # 获取验证码及其ID
    r = requests.post(url, data=datas, headers=headers)
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    # 利用bs4获得验证码图片地址
    img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
    urlretrieve(img_src, 'captcha.jpg')
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print('到本地目录打开captcha.jpg获取验证码')
    finally:
        captcha = input('please input the captcha:')
        remove('captcha.jpg')
    captcha_id = soup.find(
        'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
    return captcha, captcha_id
def isLogin():
    # 通过查看用户个人账户信息来判断是否已经登录
    url = "https://www.douban.com/accounts/"
    login_code = session.get(url, headers=headers,
                             allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False
def login():
    captcha, captcha_id = get_captcha()
    # 增加表数据
    datas['captcha-solution'] = captcha
    datas['captcha-id'] = captcha_id
    login_page = session.post(url, data=datas, headers=headers)
    page = login_page.text
    soup = BeautifulSoup(page, "html.parser")
    result = soup.findAll('div', attrs={'class': 'title'})
    #进入豆瓣登陆后页面，打印热门内容
    for item in result:
        print(item.find('a').get_text())
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()
if __name__ == '__main__':
    if isLogin():
        print('Login successfully')
    else:
        login()
#==========================================
# 知乎登录:cookies登录
#==========================================
