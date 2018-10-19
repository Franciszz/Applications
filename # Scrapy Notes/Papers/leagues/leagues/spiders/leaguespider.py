# -*- coding: utf-8 -*-
import scrapy


class LeaguespiderSpider(scrapy.Spider):
    name = 'leaguespider'
    allowed_domains = ['www.basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/']

    def parse(self, response):
        pass
