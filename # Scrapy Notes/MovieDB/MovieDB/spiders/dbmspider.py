# -*- coding: utf-8 -*-
import scrapy
from MovieDB.items import MoviedbItem

class DbmspiderSpider(scrapy.Spider):
    name = 'dbmspider'
    allowed_domains = ['movie.douban.com']
    #start_urls = ['http://https://movie.douban.com/top250']
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield scrapy.Request(url, callback = self.parse)
    def parse(self, response):
        item = MoviedbItem()
        movies = response.xpath('//div[@class="info"]')
        for movie in movies:
            title = movie.xpath('div[@class="hd"]/a/span[@class="title"][1]/text()').extract()
            link = movie.xpath('div[@class="hd"]/a/@href')
            role = movie.xpath('div[@class="bd"]/p/text()').extract()[0]
            movieInfo  = movie.xpath('div[@class="bd"]/p/text()').extract()[1]
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            number = movie.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()').extract()
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            item['title'] = title
            item['movieInfo'] = movieInfo
            item['role'] = role
            item['star'] = star
            item['number'] = number
            item['quote'] = quote
            item['link'] = link
            yield item
        nextPage = response.xpath('//span[@class="next"]/link/@href').extract()
        if nextPage:
            yield scrapy.Request(response.urljoin(str(nextPage[0])))
# 模拟登录用户
# import scrapy
#
# class LoginSpider(scrapy.Spider):
#     name = 'example.com'
#     start_urls = ['http://www.example.com/users/login.php']
#
#     def parse(self, response):
#         return scrapy.FormRequest.from_response(
#             response,
#             formdata={'username': 'john', 'password': 'secret'},
#             callback=self.after_login
#         )
#
#     def after_login(self, response):
#         # check login succeed before going on
#         if "authentication failed" in response.body:
#             self.logger.error("Login failed")
#             return
#
#         # continue scraping with authenticated session...