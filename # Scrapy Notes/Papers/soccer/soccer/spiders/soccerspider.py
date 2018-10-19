# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from soccer.items import SoccerItem
import time

class SoccerspiderSpider(scrapy.Spider):
    name = 'soccerspider'
    allowed_domains = ['www.cfadata.com']
    year = 1995
    def start_requests(self):
        return [self.next_requests()]
    def parse(self, response):
        items = SoccerItem()
        sel = Selector(response)
        seasons = sel.xpath('//div/table/tbody/tr[re:test(@style,"height:\d+\.\d+pt}")]')
        for season in seasons:
            obs = season.xpath('/td/text()').extract()
            items['rank'],items['div'],items['codeid'],items['club'],items['team'] = obs[0:5]
            items['englist'],items['plays'],items['points'],items['wins'],items['draws']= obs[5:10]
            items['loss'],items['gscores'],items['gaginst'],items['netscore'] = obs[10:14]
            items['year'] = self.year
            yield items
        self.year += 1
        time.sleep(5)
        if self.year < 2018:
            yield self.next_requests()
    def next_requests(self):
        return scrapy.http.FormRequest('http://www.cfadata.com/cfa-{}.php'.format(self.year),callback = self.parse

