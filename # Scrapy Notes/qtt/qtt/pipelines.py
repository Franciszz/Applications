# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from qtt.qttutils import QttUtils

class QttPipeline(object):
    def __init__(self):
        #获取自定义存储路径
        store_path = QttUtils.getStorepath()
        json_path = store_path+"/"+"qtt.json"
        self.filename = open(json_path,"wb")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(text.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.filename.close()