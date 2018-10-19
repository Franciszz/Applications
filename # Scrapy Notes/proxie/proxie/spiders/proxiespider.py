# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy


class ProxieSpider(scrapy.Spider):

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    name = "proxie"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://news.sina.com.cn/']

    def parse(self, response):
        print(response.body)