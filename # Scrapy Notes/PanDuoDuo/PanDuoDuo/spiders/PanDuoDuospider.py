#encoding=utf8
import scrapy
from PanDuoDuo.items import PanduoduoItem

class Panduoduo(scrapy.Spider):
    name = 'panduoduo'
    allowed_domains =['panduoduo.net']
    start_urls = ['http://www.panduoduo.net/c/4/{}'.format(n) for n in range(1,86151)]#6151
    # start_urls = ['http://www.panduoduo.net/c/4/1']#6151
    def parse(self, response):
        base_url = 'http://www.panduoduo.net'
        # print(str(response.body).encode('utf-8'))
        node_list = response.xpath("//div[@class='ca-page']/table[@class='list-resource']")
        node_list = response.xpath("//table[@class='list-resource']/tr")
        # print(node_list)
        for node  in node_list:
            duoItem = PanduoduoItem()
            title = node.xpath("./td[@class='t1']/a/text()").extract()
            print(title)
            duoItem['docName'] = ''.join(title)
            link = node.xpath("./td[@class='t1']/a/@href").extract()
            linkUrl  = base_url+''.join(link)
            duoItem['docLink'] = linkUrl
            print(linkUrl)
            docType = node.xpath("./td[2]/a/text()").extract()
            duoItem['docType'] = ''.join(docType)
            print(docType)
            docSize = node.xpath("./td[@class='t2']/text()").extract()
            print(docSize)
            duoItem['docSize'] = ''.join(docSize)
            docCount = node.xpath("./td[5]/text()").extract()
            docTime = node.xpath("./td[6]/text()").extract()
            duoItem['docCount'] = ''.join(docCount)
            duoItem['docTime'] = ''.join(docTime)
            print(docCount)
            print(docTime)
            yield duoItem