# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    province=scrapy.Field()           #省
    city = scrapy.Field()             #市
    city_href = scrapy.Field()        #市链接
    county = scrapy.Field()           #区县
    county_href = scrapy.Field()      #区县链接
    #二手房
    oldhome_href = scrapy.Field()     #区县二手房小区链接
    house = scrapy.Field()            #小区名称
    date_before=scrapy.Field()        #上月
    price = scrapy.Field()            #房价
    rate_m_unit = scrapy.Field()      #环比上月（上升或下降）
    rate_m=scrapy.Field()             #环比上月
    #新楼盘
    newhome_href=scrapy.Field()       #区县新楼盘小区链接
    newhome_fweb=scrapy.Field()       #区县新楼盘小区首页链接
    price_type=scrapy.Field()         #房价类型（起价或均价）
    time=scrapy.Field()               #房价更新时间
    cpage=scrapy.Field()              #当前页

    building = scrapy.Field()         #二手房或新楼盘
    ProgramStarttime = scrapy.Field() #爬取时间



