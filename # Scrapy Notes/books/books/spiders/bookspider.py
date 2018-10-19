# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from books.items import BooksItem

# class BookspiderSpider(scrapy.Spider):
#     name = 'bookspider'
#     allowed_domains = ['book.douban.com']
#     start_urls = ['https://book.douban.com/tag/%E5%8E%86%E5%8F%B2']
#     def parse(self, response):
#         sel = Selector(response)
#         book_list = sel.xpath('//div[@class= "info"]')
#         for book in book_list:
#             item = BooksItem()
#             item['book_name'] = book.xpath('/h2/a/text()').extract()[0].strip()
#             item['book_grade'] = book.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract().strip()
#             item['book_count'] = book.xpath('div[@class="star clearfix"]/span[@class="pl"]/text()').extract().strip()
#             item['book_desc'] = book.xpath('p/text()').extract().strip()
#             item['book_link'] = book.xpath('div[@class="ft"]/div[@class="ebook-link"]/a/@href').extract()
#             pub = book.xpath('/h2/div[@class="pub"]/text()').extract().strip().split('/')
#             item['book_price'] = pub.pop()
#             item['book_date'] = pub.pop()
#             item['book_publish'] = pub.pop()
#             item['book_auther'] = pub.pop()
#             yield item



class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['douban.com']
    def start_requests(self):
        url = 'https://book.douban.com/tag/%E5%8E%86%E5%8F%B2'
        yield scrapy.Request(url, callback = self.parse)
    def parse(self, response):
        item = BooksItem()
        book_list = response.xpath('//u1[@class="subject-list"]/li[@class="subject-item"]/div[@class= "info" ]')
        for book in book_list:
            try:
                title = book.xpath('/h2/a/text()').extract()
                pub = book.xpath('/h2/div[@class="pub"]/text()').extract().strip().split('/')
                price = pub.pop()
                date = pub.pop()
                publish = pub.pop()
                auther = '/'.join(pub)
                grade = book.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract().strip()
                count = book.xpath('div[@class="star clearfix"]/span[@class="pl"]/text()').extract().strip()
                desc = book.xpath('p/text()').extract().strip()
                link = book.xpath('div[@class="ft"]/div[@class="ebook-link"]/a/@href').extract()
                item['book_name'] = title
                item['book_auther'] = auther
                item['book_grade'] = grade
                item['book_count'] = count
                item['book_publish'] = publish
                item['book_date'] = date
                item['book_price'] = price
                item['book_desc'] = desc
                item['book_link'] = link
                yield item
            except:
                pass
        nextpage = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0].strip()
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            yield scrapy.Request(nextpage)


