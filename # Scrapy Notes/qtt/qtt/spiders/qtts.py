# -*- coding: utf-8 -*-
import scrapy
# 通过CrawlSpider,Rule类爬取
# -*-from scrapy.spiders import CrawlSpider,Rule-*-
# -*-from scrapy.linkextractors import LinkExtractor-*-
from qtt.items import QttItem
import json
import re
from qtt import qttconfig as QttConfig

class QttsSpider(scrapy.Spider):
    name = 'qtts'
    allowed_domains = ['api.1sapp.com']
    # 爬取地址
    start_urls = []
    categoryInfo = QttConfig.CATEGORY_INFO
    limit = QttConfig.LIST_LIMIT
    for value in categoryInfo:
        url = QttConfig.LIST_API + "cid=%s&tn=1&page=1&limit=%s" % (str(value['cid']), str(limit))
        start_urls.append(url)

    # 详情页
    def detail_parse(self, response):
        # 提取每次Response的meta数据
        meta_item = response.meta['meta_item']
        # 取内容
        content_selector = response.xpath('//div[@class="content"]')
        meta_item['content_images'] = content_selector.xpath('//img/@src|//img/@data-src').extract()
        meta_item['content'] = content_selector.extract()[0]
        yield meta_item
    # response里链接的提取规则
    # -*-pageLink = LinkExtractor(allow=("start=\d+"))-*-
    # -*-rules = [
    # -*-   #用pageLink提取规则跟进，通过parseQtt进行解析
    # -*-   Rule(pageLink,callback="parseQtt",follow=True)
    # -*-]
    def parse(self, response):
        response_url = response.url
        # 分类id从url又获取了一次
        searchObj = re.search(r'(.*)cid=(\d+)', response_url)
        cid = searchObj and searchObj.group(2) or 0

        data = json.loads(response.text)['data']['data']

        for value in data:
            # 初始化模型对象
            item = QttItem()
            # 来源
            item['source_name'] = value['source_name']
            # 标题
            item['title'] = value['title']
            # 详细页url
            url = item['url'] = value['url']
            # url = url[0:url.find('?')]
            # 简介
            item['introduction'] = value['introduction']
            # 封面图
            item['cover'] = value['cover']
            # 发布时间
            item['publish_time'] = value['publish_time']
            # 分类
            item['cid'] = cid

            # 爬取详情页
            yield scrapy.Request(url=item['url'], meta={'meta_item': item}, callback=self.detail_parse)



