import requests
import random
import time
from bs4 import BeautifulSoup
import lxml
from lxml import etree
# ===================================================================================
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
# ======================= 中乙运动员 =================================================
url_0 = 'https://zh.wikipedia.org/wiki/Category:%E4%B8%AD%E4%B9%99%E7%90%83%E5%91%98'

def get_url(url):
    res = requests.get(url, headers = myheader)
    res.encoding = 'utf8'
    tree = etree.HTML(res.text)
    urls = tree.xpath('//div[@class="mw-category-group"]//li/a/@href')
    return urls
urls = ['https://zh.wikipedia.org'+ url for url in get_url(url_0)]
info_list = []
nation_list = []
for url in urls[-3:]:
    res = requests.get(url, headers=myheader)
    time.sleep(0.5)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    tab =  tree.xpath('//div/table[@class="infobox vcard"]')[0]
    name = tab.xpath('caption/b/text()')[0]
    #name = tree.xpath('//div/table[@class="infobox vcard"]//th[text()="全名"]/../td/span/text()')[0]
    birthdate = tab.xpath('//th[text()="出生日期"]/../td/text()')
    birthplace = tab.xpath('//th[text()="出生地点"]/../td/a/text()')
    height = tab.xpath('//th[text()="身高"]/../td/text()')
    position = tab.xpath('//th[text()="位置"]/../td/text()')+tab.xpath('//th[text()="位置"]/../td/a/text()')
    teen = tab.xpath('//th[text()="青年"]')
    if teen:
        teen_team = tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/text()')+\
                    tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/a/text()')
    else:
        teen_team = []
    if birthdate:
        birthdate = birthdate[0]
    #if birthplace:
    #    birthplace = ['-'.join(ele) for ele in birthplace][0]
    if height:
        height = height[0]
    #if position == []:
    #    position = tab.xpath('//th[text()="位置"]/../td/a/text()')
    club_per = tab.xpath('//th[text()="职业俱乐部*"]/../following-sibling::tr')
    club_cou = tab.xpath('//th[contains(text(),"国家队")]/../following-sibling::tr')
    if club_per:
        club_last = tab.xpath('//th[contains(text(),"职业俱乐部*")]/../following-sibling::tr')[-1]
        if club_cou:
            for ele in club_cou:
                club_per.remove(ele)
            club_per = club_per[:-1]
        else:
            club_per.remove(club_last)
    for tr in club_per[1:]:
        per_time = tr.xpath('th/span/text()')
        per_team = tr.xpath('td/a/text()')
        per_tick = tr.xpath('td/text()')
        info = [name, birthdate, birthplace, height, position, teen_team, per_time, per_team, per_tick]
        print(info)
        info_list.append(info)
    if club_cou:
        for tr in club_cou[:-1]:
            nation_time = tr.xpath('th/span/text()')
            nation_team = tr.xpath('td/a/text()')
            nation_tick = tr.xpath('td/text()')
            info_nation = [name, nation_time, nation_team, nation_tick]
            print(info_nation)
            nation_list.append(info_nation)
info_pd_zy = pd.DataFrame(info_list)
info_pd_zy.to_excel('info_pd_zy.xlsx')
nation_pd_zy = pd.DataFrame(nation_list)
nation_pd_zy.to_excel('nation_pd_zy.xlsx')
# ======================= 中甲运动员 =================================================
url_1 = ['https://zh.wikipedia.org/wiki/Category:%E4%B8%AD%E7%94%B2%E7%90%83%E5%91%98',
         'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E7%94%B2%E7%90%83%E5%91%98&pagefrom=Kilama%2C+Jean-Jacques%0A%E5%B0%9A%E9%9B%85%E5%85%8B%C2%B7%E5%9F%BA%E8%97%8D%E9%A6%AC#mw-pages',
         'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E7%94%B2%E7%90%83%E5%91%98&pagefrom=SUN+Bo%0A%E5%AD%99%E9%93%82#mw-pages',
         'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E7%94%B2%E7%90%83%E5%91%98&pagefrom=%E6%88%88%E5%85%B0%C2%B7%E6%88%88%E5%9F%BA%E5%A5%87#mw-pages']
url_list = []
for url in url_1:
    url_list += ['https://zh.wikipedia.org'+ url1 for url1 in get_url(url)]
#info_list_zj = []
#nation_list_zj = []
for url in url_list:
    res = requests.get(url, headers=myheader)
    time.sleep(0.5)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    tab =  tree.xpath('//div/table[@class="infobox vcard"]')[0]
    name = tab.xpath('caption/b/text()')[0]
    #name = tree.xpath('//div/table[@class="infobox vcard"]//th[text()="全名"]/../td/span/text()')[0]
    birthdate = tab.xpath('//th[text()="出生日期"]/../td/text()')
    birthplace = tab.xpath('//th[text()="出生地点"]/../td/a/text()')
    height = tab.xpath('//th[text()="身高"]/../td/text()')
    position = tab.xpath('//th[text()="位置"]/../td/text()')+tab.xpath('//th[text()="位置"]/../td/a/text()')
    teen = tab.xpath('//th[text()="青年"]')
    if teen:
        teen_team = tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/text()')+\
                    tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/a/text()')
    else:
        teen_team = []
    if birthdate:
        birthdate = birthdate[0]
    #if birthplace:
    #    birthplace = ['-'.join(ele) for ele in birthplace][0]
    if height:
        height = height[0]
    #if position == []:
    #    position = tab.xpath('//th[text()="位置"]/../td/a/text()')
    club_per = tab.xpath('//th[text()="职业俱乐部*"]/../following-sibling::tr')
    club_cou = tab.xpath('//th[contains(text(),"国家队")]/../following-sibling::tr')
    if club_per:
        club_last = tab.xpath('//th[contains(text(),"职业俱乐部*")]/../following-sibling::tr')[-1]
        if club_cou:
            for ele in club_cou:
                club_per.remove(ele)
            club_per = club_per[:-1]
        else:
            club_per.remove(club_last)
    for tr in club_per[1:]:
        per_time = tr.xpath('th/span/text()')
        per_team = tr.xpath('td/a/text()')
        per_tick = tr.xpath('td/text()')
        info = [name, birthdate, birthplace, height, position, teen_team, per_time, per_team, per_tick]
        print(info)
        info_list_zj.append(info)
    if club_cou:
        for tr in club_cou[:-1]:
            nation_time = tr.xpath('th/span/text()')
            nation_team = tr.xpath('td/a/text()')
            nation_tick = tr.xpath('td/text()')
            info_nation = [name, nation_time, nation_team, nation_tick]
            print(info_nation)
            nation_list_zj.append(info_nation)
info_pd_zj = pd.DataFrame(info_list_zj)
info_pd_zj.to_excel('info_pd_zj.xlsx')
nation_pd_zj = pd.DataFrame(nation_list_zj)
nation_pd_zj.to_excel('nation_pd_zj.xlsx')


url_list.index('https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%A3%AE%E9%A3%9E')


# ======================= 中超运动员 =================================================
url_2 = [
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98',
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98&pagefrom=Festus+Baise%0A%E6%B3%95%E5%9C%96%E6%96%AF%C2%B7%E6%8B%9C%E6%96%AF#mw-pages',
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98&pagefrom=Lei%2C+Tenglong%0A%E9%9B%B7%E8%85%BE%E9%BE%99#mw-pages',
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98&pagefrom=Odita%2C+Obiora%0A%E5%A5%A5%E6%AF%94%E5%A5%A5%E6%8B%89%C2%B7%E5%A5%A5%E5%90%89%E5%A1%94#mw-pages',
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98&pagefrom=WANG+Dalei%0A%E7%8E%8B%E5%A4%A7%E9%9B%B7#mw-pages',
    'https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E8%B6%85%E7%90%83%E5%91%98&pagefrom=ZHANG+Xincheng%0A%E5%BC%A0%E9%91%AB%E6%88%90#mw-pages'
]
url_list_zc = []
name_list_zc = []
def get_url(url, url_re = True):
    res = requests.get(url, headers = myheader)
    res.encoding = 'utf8'
    tree = etree.HTML(res.text)
    urls = tree.xpath('//div[@class="mw-category-group"]//li/a/@href')
    names = tree.xpath('//div[@class="mw-category-group"]//li/a/text()')
    if url_re:
        return urls
    else:
        return names
for url in url_2:
    url_list_zc += ['https://zh.wikipedia.org'+ url1 for url1 in get_url(url, url_re= True)]
    name_list_zc += get_url(url, url_re= False)
info_com_list = []
info_com_name = []
info_tick_list = []
nation_com_list = []
info_list_zc = []
nation_list_zc = []
for url in url_list_zc[1105:]:
 #   url = 'https://zh.wikipedia.org/wiki/%E5%86%AF%E7%BB%8D%E9%A1%BA'
    res = requests.get(url, headers=myheader)
    res.encoding = 'utf-8'
    tree = lxml.etree.HTML(res.content)
    tab =  tree.xpath('//div/table[@class="infobox vcard"]')
    if tab:
        tab = tab[0]
        name = tab.xpath('caption/b/text()')
        birthdate = tab.xpath('//th[text()="出生日期"]/../td/text()')
        birthplace = tab.xpath('//th[text()="出生地点"]/../td/a/text()')
        height = tab.xpath('//th[text()="身高"]/../td/text()')
        position = tab.xpath('//th[text()="位置"]/../td/text()') + tab.xpath('//th[text()="位置"]/../td/a/text()')
        teen = tab.xpath('//th[text()="青年"]')
        if name:
            name = name[0]
        if teen:
            teen_team = tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/text()') + \
                        tab.xpath('//th[text()="青年"]/../following-sibling::tr[1]/td/a/text()')
        else:
            teen_team = []
        if birthdate:
            birthdate = birthdate[0]
        if height:
            height = height[0]
        club_per = tab.xpath('//th[text()="职业俱乐部*"]/../following-sibling::tr')
        club_cou = tab.xpath('//th[contains(text(),"国家队")]/../following-sibling::tr')
        if club_per:
            club_last = tab.xpath('//th[contains(text(),"职业俱乐部*")]/../following-sibling::tr')[-1]
            if club_cou:
                for ele in club_cou:
                    club_per.remove(ele)
                club_per = club_per[:-1]
            else:
                club_per.remove(club_last)
        for tr in club_per[1:]:
            per_time = tr.xpath('th/span/text()')
            if per_time:
                per_team = tr.xpath('td/a/text()')
                per_tick = tr.xpath('td/text()')
                # per_out = []
                # per_score = []
                # if per_tick:
                #     per_out = per_tick[0]
                #     per_score = per_tick[1]
                info = [name, birthdate, birthplace, height, position, teen_team, per_time, per_team, per_tick]
                print(info)
                info_list_zc.append(info)
                if club_cou:
                    for tr in club_cou[:-1]:
                        nation_time = tr.xpath('th/span/text()')
                        nation_team = tr.xpath('td/a/text()')
                        nation_tick = tr.xpath('td/text()')
                        # nation_out = []
                        # nation_score = []
                        # if nation_tick:
                        #     nation_out = nation_tick[0]
                        #     nation_score = nation_tick[1]
                        info = [name, nation_time, nation_team, nation_tick]
                        print(info)
                        nation_list_zc.append(info)
            else:
                name_list_zc.append(name)
                per_time = tr.xpath('th/span/span/text()')
                per_team = tr.xpath('td[1]/span/a/text()')
                per_tick = tr.xpath('td[2]/span/text()')
                info_tick_list.append(per_tick)
                #per_out = tr.xpath('td[1]/span/text()')
                #per_score = tr.xpath('td[2]/span/text()')
                for i in range(0,len(per_time)):
                    try:
                        info = [name, birthdate, birthplace, height, position, teen_team, per_time[i], per_team[i]]
                        info_com_list.append(info)
                        print(info)
                    except IndexError as e:
                        pass
                if club_cou:
                    for tr in club_cou[:-1]:
                        nation_time = tr.xpath('th/span/span/text()')
                        nation_team = tr.xpath('td/span/a/text()')
                        nation_tick = tr.xpath('td/span/text()')
                        for i in range(0, len(nation_time)):
                            try:
                                info = [name, nation_time, nation_team[i], nation_tick[i]]
                                nation_com_list.append(info)
                                print(info)
                            except IndexError as e:
                                pass
        else:
            pass
import pandas as pd
info_pd_zcc_com = pd.DataFrame(info_com_list)
info_pd_zcc_com.to_excel('info_pd_zcc_com.xlsx')
info_pd_zcc = pd.DataFrame(info_list_zc)
info_pd_zcc.to_excel('info_pd_zcc.xlsx')
info_pd_zcc_nation = pd.DataFrame(nation_com_list)
info_pd_zcc_nation.to_excel('info_pd_zcc_nation.xlsx')
info_pd_zc_nation = pd.DataFrame(nation_list_zc)
info_pd_zc_nation.to_excel('info_pd_zc_nation.xlsx')
pd.DataFrame(info_tick_list).to_excel('info_list_tick.xlsx')
pd.DataFrame(info_com_name).to_excel('info_list_name.xlsx')