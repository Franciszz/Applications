# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field

class OldhouseItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dist_region = Field()
    dist_name = Field()
    building = Field()
    direction = Field()
    decoration = Field()
    year = Field()
    price_total = Field()
    price = Field()
    price_dist = Field()
    room_type = Field()
    room_area = Field()
    link = Field()
    pass



