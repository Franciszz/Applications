import requests
import random
import time
from bs4 import BeautifulSoup
import pandas as pd
import lxml
from lxml import etree
# ==============================================================================
# ==================== 获取足球队比赛url
# ==============================================================================
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url_adult = 'http://wiki.cfadata.com/index.php?title=%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E7%94%B7%E5%AD%90%E8%B6%B3%E7%90%83%E9%98%9F%E6%AF%94%E8%B5%9B%EF%BC%881999%EF%BC%89'
url_teen = 'http://wiki.cfadata.com/index.php?title=%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E7%94%B7%E5%AD%90%E9%9D%92%E5%B0%91%E5%B9%B4%E8%B6%B3%E7%90%83%E9%98%9F%E6%AF%94%E8%B5%9B%EF%BC%881999%EF%BC%89'
url_list_adult = []
url_list_teen = []
res = requests.get(url_adult, headers = myheader)
res.encoding = 'utf-8'
tree = lxml.etree.HTML(res.text)
years = tree.xpath('//td[@class="roundy bl-超级 bw-1 at-l"]/p/a/text()')[-19:]
url_list_adult = ['http://wiki.cfadata.com'+ url for url in tree.xpath('//td[@class="roundy bl-超级 bw-1 at-l"]/p/a/@href')[-19:]]
res = requests.get(url_teen, headers = myheader)
res.encoding = 'utf-8'
tree = lxml.etree.HTML(res.text)
url_list_teen = ['http://wiki.cfadata.com' + url for url in tree.xpath('//td[@class="roundy bl-超级 bw-1 at-l"]/p/a/@href')[-19:]]
urldict = {
    'years': years,
    'adult': url_list_adult,
    'teen': url_list_teen
}
urldict
# ==============================================================================
# ==================== 获取青年男子足球队数据
# ==============================================================================
url_t_0 = url_list_teen[-1]
res = requests.get(url_t_0, headers = myheader)
res.encoding = 'utf-8'
tree = lxml.etree.HTML(res.content)
tocs = tree.xpath('//div[@id = "toc"]/ul/li')
game_dict = {
    'years': [],
    'level': [],
    'gamelist':[]
}
# ======  tem content ================##############
#content_list = []
#content_adult = []
for i in range(len(urldict['years'])):
    url = urldict['teen'][i]
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    time.sleep(random.randint(1, 3))
    content_list.append(res.content)
for i in range(len(urldict['years'])):
    url = urldict['adult'][i]
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    time.sleep(random.randint(1, 2))
    content_adult.append(res.content)
# ====================================##############
nation_game_teen = []
for i in range(19):#len(urldict['years'])):
    year = urldict['years'][i]
    url = urldict['teen'][i]
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    tocs = tree.xpath('//div[@id = "toc"]/ul/li')
    for toc in tocs:
        level = toc.xpath('a/span[2]/b/text()')
        game_list = toc.xpath('ul/li/a/span[2]/text()')
        #game_dict['years'].append(year)
        #game_dict['level'].append(level)
        #game_dict['gamelist'].append(game_list)
        for game in game_list:
            print(game)
            tabs = tree.xpath('//h3/span[text()="{}"]/../following-sibling::table[1][1]//tr'.format(game))[1::2]
            for tab in tabs:
                game_info = tab.xpath('td/text()')
                lis = tab.xpath('following-sibling::tr[1][1]/td/ul/li')
                for li in lis:
                    player = li.xpath('text()')
                    name_list = [year, level, game_info, player]
                    print(name_list)
                    nation_game_teen.append(name_list)
nation_game_teen_pd = pd.DataFrame(nation_game_teen)
nation_game_teen_pd.to_excel('nation_game_teen.xlsx')
nation_game_teen_com = []
for i in range(2,6):#len(urldict['years'])):
    year = urldict['years'][i]
    url = urldict['teen'][i]
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    tocs = tree.xpath('//div[@id = "toc"]/ul/li')
    for toc in tocs:
        level = toc.xpath('a/span[2]/b/text()')[0]
        print(level)
        tabs = tree.xpath('//h2/span/b/[text()="{}"]/ancestor/following-sibling::table[1][1]//tr'.format(level))#[1::2]
        print(tabs)
        for tab in tabs:
            game_info = tab.xpath('td/text()')
            lis = tab.xpath('following-sibling::tr[1][1]/td/ul/li')
            for li in lis:
                player = li.xpath('text()')
                name_list = [year, level, game_info, player]
                print(name_list)
                nation_game_teen_com.append(name_list)
# ======= 国足 ====================================================================================
 nation_game_adult = []
for i in range(19):
    year = urldict['years'][i]
    url = urldict['adult'][i]
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    if (i > 1) & (i < 14):
        print(i)
        game_list = tree.xpath('//div[@id="mw-content-text"]/table//tr[@align="center"]')[1:]
        for game in game_list:
            game_info = game.xpath('td/text()')
            for li in game.xpath('following-sibling::tr[1]/td/ul/li'):
                nation_game = [year, game_info, li.xpath('text()')]
                nation_game_adult.append(nation_game)
                print(nation_game)
    else:
        game_list = tree.xpath('//div[@class="toccolours mw-collapsible mw-collapsed"]')
        for game in game_list:
            game_time = game.xpath('table//td[2]/text()')[1]
            game_position = game.xpath('table//td[6]/text()')[0]
            game_name = game.xpath('table//td[2]/span/b/text()')[0]
            game_oppo = game.xpath('table//td[3]/text()')[0]+game.xpath('table//td[5]/text()')[0]
            game_score = game.xpath('table//td[4]/b/text()')[0]
            game_info = [game_time, game_position, game_name, game_oppo, game_score]
            game_player = game.xpath('div/table[2]//tr/td/a/text()')
            nation_game = [year, game_info, game_player]
            nation_game_adult.append(nation_game)
            print(nation_game)
nation_game_adult = pd.DataFrame(nation_game_adult)
nation_game_adult.to_excel('nation_game_adult.xlsx')


