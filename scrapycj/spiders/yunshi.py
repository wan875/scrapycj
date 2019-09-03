# -*- coding: utf-8 -*-
import scrapy
from scrapycj.items import YunshiItem


class YunshiSpider(scrapy.Spider):
    name = 'yunshi'
    allowed_domains = ['yunshi24.com']
    start_urls = ['http://www.yunshi24.com/']

    def parse(self, response):
        for box in response.xpath('//main[contains(@class,"ullist")]/ul/li'):
            item = YunshiItem()
            item['title'] = box.xpath('div[contains(@class,"con")]/h4/a/text()').extract()[0]
            #item['content'] = ''
            item['url'] = 'http://www.yunshi24.com' + box.xpath('div[contains(@class,"con")]/h4/a/@href').extract()[0]
            item['thum'] = box.xpath('a[contains(@class,"img-cover")]/img/@src').extract()[0]
            item['source'] = '陨石财经'
            item['type'] = '2'

            #yield item
            # yield item
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parseinfo, dont_filter=True)


    def parseinfo(self,response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[contains(@class,"art-4")]').extract()[0]
        yield item