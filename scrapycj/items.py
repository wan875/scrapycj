# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapycjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class YunshiItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    thum = scrapy.Field()
    source = scrapy.Field()
    type = scrapy.Field()