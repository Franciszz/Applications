# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章id
    aid = scrapy.Field()
    # 来源
    source_name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 详细页url
    url = scrapy.Field()
    # 简介
    introduction = scrapy.Field()
    # 封面图
    cover = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 分类ID
    cid = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 内容-中的图片
    content_images = scrapy.Field()
