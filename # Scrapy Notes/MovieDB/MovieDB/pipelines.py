# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class MoviedbPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port = 3306,
                                    user = 'root',
                                    password = 'root',
                                    db = 'scrapy',
                                    charset = 'utf8')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate table Moive')
        # self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute('insert into MovieDB (mname,info,role,star,comment,quote) VALUES (%s, %s, %s, %s, %s, %s)',
                                (item['title'],item['movieInfo'], item['role'], item['star'], item['number'], item['quote']))
            self.conn.commit()
        except pymysql.Error:
            print('Error %s, %s, %s, %s, %s, %s ' % (item['title'],item['movieInfo'], item['role'], item['star'], item['number'], item['quote']))
        return item

