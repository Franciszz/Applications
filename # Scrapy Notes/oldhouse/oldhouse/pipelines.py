# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class OldhousePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    password='root',
                                    db='scrapy',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate table house')
        # self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                'insert into house (dist_region,dist_name,building,direction,decoration,room_year,'
                'price_total,price,price_dist,room_area,room_type,link) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (item['dist_name'],item['dist_region'],item['building'],item['direction'],
                 item['decoration'],item['year'],item['price_total'],item['price'],
                 item['price_dist'],item['room_type'],item['room_area'],item['link']))
            self.conn.commit()
        except pymysql.Error:
            print('Sorry.')
        return item



