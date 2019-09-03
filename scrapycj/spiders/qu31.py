# -*- coding: utf-8 -*-
import scrapy
from scrapycj.items import YunshiItem


class Qu31Spider(scrapy.Spider):
    name = 'qu31'
    allowed_domains = ['31qu.cn']
    start_urls = ['https://31qu.cn/']

    def parse(self, response):
        for box in response.xpath('//div[contains(@class,"news_item_wrap")][1]/div'):
            item = YunshiItem()
            item['title'] = box.xpath('div[contains(@class,"item_content")]/div[contains(@class,"item_summary")]/h3/a/text()').extract()[0]
            #item['content'] = ''
            item['url'] = 'https://31qu.cn' + box.xpath('a[contains(@class,"item_image")]/@href').extract()[0]
            item['thum'] = ''#box.xpath('a[contains(@class,"item_image")]/div/i').extract()
            item['source'] = '31区'
            item['type'] = '2'

            # yield item
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parseinfo, dont_filter=True)

    def parseinfo(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[contains(@class,"page_content")]//div[contains(@class,"article_wrap")][1]').extract()[0]
        yield item