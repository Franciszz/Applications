# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.conf import settings

class PanduoduoPipeline(object):
    def process_item(self, item, spider):
        return item

class DuoDuoMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = self.client[settings['MONGO_DB']]
        self.post = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        postItem = dict(item)
        self.post.insert(postItem)
        return item

