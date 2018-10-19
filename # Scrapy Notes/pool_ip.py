import urllib.request
from lxml import etree
import time
# 构造请求代理ip网站链接
def get_url(url):
    url_list = []
    for i in range(1,5):
        url_new = url+str(i)
        url_list.append(url_new)
    return url_list

# 获取网页内容
def get_content(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    header = {'User-Agent': user_agent}
    req = urllib.request.Request(url=url, headers=header)
    res = urllib.request.urlopen(req)
    content = res.read()
    return content.decode('utf-8')

# 提取网页中的ip地址和端口号信息
def get_info(content):
    datas_ip = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[2]/text()')
    datas_port = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[3]/text()')
    with open("data_1.txt", "w") as fd:
        for i in range(0, len(datas_ip)):
            out = u""
            out += u"" + datas_ip[i]
            out += u":" + datas_port[i]
            fd.write(out + u"\n")
# 验证ip的有效性
def verif_ip(ip,port):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    header = {'User-Agent': user_agent}
    proxy = {'http': 'http://%s:%s'%(ip,port)}
    print(proxy)

    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

    test_url = 'https://www.baidu.com'
    req = urllib.request.Request(url=test_url, headers=header)
    time.sleep(6)
    try:
        res = urllib.request.urlopen(req)
        time.sleep(3)
        content = res.read()
        if content:
            print('that is ok')
            with open('data_2.txt','a') as fd:
                fd.write(ip+u':'+port)
                fd.write('\n')
        else:
            print('this one is not ok')
    except urllib.request.URLError as e:
        print(e.reason)
# 调用函数
if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    url_list = get_url(url)
    for i in url_list:
        print(i)
        content = get_content(i)
        time.sleep(3)
        get_info(content)
    with open('data_1.txt','r') as fd:
        datas = fd.readlines()
        for data in datas:
            print(data.split(u':')[0])
            verif_ip(data.split(u':')[0],data.split(u':')[1])
