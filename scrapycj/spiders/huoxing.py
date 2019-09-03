# -*- coding: utf-8 -*-
import scrapy
from scrapycj.items import YunshiItem


class HuoxingSpider(scrapy.Spider):
    name = 'huoxing'
    allowed_domains = ['huoxing24.com']
    start_urls = ['https://news.huoxing24.com/']

    def parse(self, response):
        for box in response.xpath('//div[contains(@class,"news-list-wrapper")]/div[contains(@class,"news-list-item")]'):
            item = YunshiItem()
            item['title'] = box.xpath('div[contains(@class,"item-right")]/a/h5/text()').extract()[0]
            #item['content'] = ''
            item['url'] = box.xpath('a[contains(@class,"item-left")]/@href').extract()[0]
            item['thum'] = box.xpath('a[contains(@class,"item-left")]/div/img/@data-src').extract()[0]
            item['source'] = '火星财经'
            item['type'] = '2'

            # yield item
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parseinfo, dont_filter=True)

    def parseinfo(self, response):
        item = response.meta['item']
        item['content'] = \
        response.xpath('//div[contains(@class,"news-content")]').extract()[0]
        yield item