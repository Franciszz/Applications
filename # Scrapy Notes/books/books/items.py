# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = Field()
    book_auther = Field()
    book_grade = Field()
    book_count = Field()
    book_publish = Field()
    book_date = Field()
    book_price = Field()
    book_desc = Field()
    book_link = Field()
    pass
