import pymysql
import pandas as pd
import re
# 从数据库中读取二手房数据
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',
                       password='root',db='scrapy',charset='utf8')
sql = 'Select * from house'
house_sz = pd.read_sql(sql, conn)
# 数据处理
house_2=house_sz.drop(house_sz.columns[0],axis=1,inplace=False)
def cut_room_year(word,n):
    word = int(word[:n])
    return word
house_2.room_year = house_2.room_year.apply(cut_room_year,n=4)
def price_cut(word):
    comment = re.compile(r'\d+')
    word  = comment.findall(word)[0]
    return word
house_2.price = house_2.price.apply(price_cut)
house_2.price_dist = house_2.price_dist.apply(price_cut)
def area_cut(word):
    comment = re.compile(r'\d+.\d+')
    word  = comment.findall(word)
    if word:
        return word[0]
    else:
        return None
house_2.room_type = house_2.room_type.apply(area_cut)
def dist_split(word,out=1):
    district = word.split('-')[0]
    location = word.split('-')[1].split(' ')[0]
    address = word.split('-')[1].split(' ')[1]
    if out==1:
        return district
    if out==2:
        return location
    else:
        return address
house_2['district'] =  house_2.dist_name.apply(dist_split,out=1)
house_2['location'] =  house_2.dist_name.apply(dist_split,out=2)
house_2['address'] =  house_2.dist_name.apply(dist_split,out=3)
house_2['link'] = 'https://sz.centanet.com'+house_2.link
