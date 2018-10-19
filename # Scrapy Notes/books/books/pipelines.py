# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Set foreign_key_checks=0;
# Create table books (
# 	`id` int not NULL auto_increment,
# 	`name` varchar(255) default null,
# 	`auther` varchar(20) default null,
# 	`grade` varchar(10) default null,
# 	`count` varchar(20) default null,
# 	`price` varchar(20) default null,
# 	`publish` datetime default null,
# 	`introduction` varchar(1024) default null,
# 	`link` varchar(1024) default null,
# 	primary key (`id`)
# )   ENGINE=InnoDB default charset = utf8;


import pymysql
class BooksPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port = 3306,
                                    user = 'root',
                                    password = 'root',
                                    db = 'scrapy',
                                    charset = 'utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute('insert in books (name, auther, grade, count, price, publish,'
                                ' introduction, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (item['book_name'], item['book_auther'], item['book_grade'], item['book_count'],item['book_publish'],
                                 item['book_date'], item['book_price'], item['book_desc'], item['book_link'],))
            self.conn.commit()
        except pymysql.Error:
            print('Error.')
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
