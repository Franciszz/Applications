# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PanduoduoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 文件名称
    docName = scrapy.Field()
    # 文件链接
    docLink = scrapy.Field()
    # 文件分类
    docType = scrapy.Field()
    # 文件大小
    docSize = scrapy.Field()
    # 网盘类型
    docPTpye = scrapy.Field()
    # 浏览量
    docCount = scrapy.Field()
    # 收录时间
    docTime = scrapy.Field()