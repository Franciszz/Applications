# -*- coding: utf-8 -*-
import scrapy
from oldhouse.items import OldhouseItem
import time
class OldhousespiderSpider(scrapy.Spider):
    name = 'oldhousespider'
    allowed_domains = ['sz.centanet.com']
    start_urls = ['sz.centanet.com/ershoufang/']
    url = 'https://sz.centanet.com/ershoufang/'
    curPage = 2
    def start_requests(self):
        return [self.next_request()]
    def parse(self, response):
        item = OldhouseItem()
        houses = response.xpath('//div[@class="house-item clearfix"]')
        for house in houses:
            # 获取小区名称
            district_name = house.xpath('div[@class="item-info fl"]/p[@class="house-name"]/a/text()').extract()
            # 获取小区地址
            district_region = house.xpath('div[@class="item-info fl"]/p[@class="house-txt"][2]/span/text()').extract()
            # 获取楼层建筑
            building = house.xpath('div[@class="item-info fl"]/p[@class="house-txt"][1]/span[1]/text()').extract()
            # 获取房间朝向
            direction = house.xpath('div[@class="item-info fl"]/p[@class="house-txt"][1]/span[2]/text()').extract()
            # 获取房间装修类型
            decoration = house.xpath('div[@class="item-info fl"]/p[@class="house-txt"][1]/span[3]/text()').extract()
            # 获取房间建造年份
            year = house.xpath('div[@class="item-info fl"]/p[@class="house-txt"][1]/span[4]/text()').extract()
            # 获取房间总价
            price_total = house.xpath('div[@class="item-pricearea fr"]/p[@class="price-nub cRed tc"]/span/text()').extract()
            # 获取房间均价
            price = house.xpath('div[@class="item-pricearea fr"]/p[@class="price-txt tc"]/text()').extract()
            # 获取所在小区均价
            price_dist = house.xpath('div[@class="item-pricearea fr"]/p[@class="price-txtB tc"]/text()').extract()
            # 获取房间类型
            room_type = house.xpath('div[@class="item-info fl"]/p[@class="house-name"]/span[3]/text()').extract()
            # 获取房间面积
            room_area = house.xpath('div[@class="item-info fl"]/p[@class="house-name"]/span[5]/text()').extract()
            ###获取房间链接
            link = house.xpath('div[@class="item-info fl"]/h4[@class="house-title"]/a/@href').extract()
            item['dist_name'] = district_name
            item['dist_region'] = district_region
            item['building'] = building
            item['direction'] = direction
            item['decoration'] = decoration
            item['year'] = year
            item['price_total'] = price_total
            item['price'] = price
            item['price_dist'] = price_dist
            item['room_type'] = room_type
            item['room_area'] = room_area
            item['link'] = link
            yield item
        self.curPage += 1
        time.sleep(5)
        yield self.next_request()
        # nextPage = response.xpath('//div[@class="page-box"]/div[@class="page-inner"]/a[@class="fsm fb"]/@href').extract()
        # if nextPage:
        #     yield scrapy.Request('https://sz.centanet.com'+str(nextPage[0]))
    def next_request(self):
        return scrapy.http.FormRequest(self.url+("g%d/"% self.curPage), callback=self.parse)

    # def start_requests(self):
    #     return [scrapy.FormRequest("http://www.example.com/login",
    #                                formdata={'user': 'john', 'pass': 'secret'},
    #                                callback=self.logged_in)]
    # def logged_in(self, response):
    #     # here you would extract links to follow and return Requests for
    #     # each of them, with another callback
    #     pass