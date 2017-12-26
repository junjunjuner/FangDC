# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city=scrapy.Field()
    city_pinyin=scrapy.Field()
    room=scrapy.Field()
    floor = scrapy.Field()
    location = scrapy.Field()
    area = scrapy.Field()
    date = scrapy.Field()
    total_price = scrapy.Field()
    price = scrapy.Field()
    source=scrapy.Field()
    city_url=scrapy.Field()