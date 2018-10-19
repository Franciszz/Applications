# -*- coding: utf-8 -*-
import scrapy
from dbbooks.items import DbbooksItem

class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanspider'
    allowed_domains = ['https://read.douban.com/']
    #start_urls = ['http://https://read.douban.com//']
    def start_requests(self):
        url = 'https://read.douban.com/kind/114'
        yield scrapy.Request(url, callback = self.parse)
    def parse(self, response):
        item = DbbooksItem()
        info_list = response.xpath('//ul[@class="list-lined ebook-list column-list"]/li[@class="item store-item"]/div[@class="info"]')
        print(info_list)
        for info in info_list:
            item['book_name'] = info.xpath('/div[@class="title"]/a/text()').extract()
            item['book_type'] = info.xpath('/p[2]/span[@class="category"]/span[@class="labeled_text"]/a/text()').extract()
            item['book_auther'] = info.xpath('/p[1]/span/span[@class="labeled_text"]/a/text()').extract()
            item['book_count'] = info.xpath('/div[@class="rating amount"]/a[@class="rating-link"]/span/text()').extract()
            item['book_grade'] = info.xpath('/div[@class="rating list-rating"]/span[@class="rating-average"]/text()').extract()
            item['book_ind'] = info.xpath('/div[@class="article-desc-brief"]/text()').extract()
            item['book_link'] = info.xpath('/div[@class="title"]/a/@href').extract()
            yield item
        next_temp_url = response.xpath('//li[@class="next"]/a/@href').extract()
        if next_temp_url:
            yield scrapy.Request(response.urljoin(str(next_temp_url[0])),callback=self.parse)
        pass

