# -*- coding: utf-8 -*-
import scrapy
from scrapycj.items import YunshiItem


class HuoxingSpider(scrapy.Spider):
    name = 'odaily'
    allowed_domains = ['odaily.com']
    start_urls = ['https://www.odaily.com/']

    def parse(self, response):
        for box in response.xpath('//div[contains(@class,"_2Ab2GT-r")]/div[contains(@class,"_1Bst2TaA")]'):
            item = YunshiItem()
            item['title'] = box.xpath('div[contains(@class,"_2ewbxSgU")]/a/h3/text()').extract()[0]
            #item['content'] = ''
            item['url'] =  'https://www.odaily.com'+box.xpath('div[contains(@class,"_2ewbxSgU")]/a/@href').extract()[0]
            item['thum'] = box.xpath('div[1]/a/@style').extract()[0].replace('background-image: ','').replace('url','').replace('("','').replace('");','').replace('!heading','')
            item['source'] = '星球日报'
            item['type'] = '2'

            #yield item
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parseinfo, dont_filter=True)

    def parseinfo(self, response):
        item = response.meta['item']
        item['content'] = \
        response.xpath('///html/body/div[1]/div[3]/div[1]/article/div[1]/div[2]').extract()[0]
        yield item