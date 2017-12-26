# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    province=scrapy.Field()               #省
    city=scrapy.Field()                   #市
    city_href=scrapy.Field()              #市链接
    county=scrapy.Field()                 #区县
    county_href=scrapy.Field()            #区县链接

    #二手房
    date_range=scrapy.Field()             #上三个月
    number = scrapy.Field()               #出售数量
    value = scrapy.Field()                #市场价值
    date_last = scrapy.Field()            #近一个月
    price_last=scrapy.Field()             #近一月平均单价
    rate_ml_unit=scrapy.Field()           #环比上月(上升或下降)
    rate_ml=scrapy.Field()                #环比上月
    add_last = scrapy.Field()             #近一月新增出售房源
    date_before = scrapy.Field()          #上一个月
    rate_y_unit=scrapy.Field()            #同比去年(上升或下降)
    rate_y = scrapy.Field()               #同比去年
    price_before = scrapy.Field()         #上月出售平均单价
    totalprice_before = scrapy.Field()    #上月出售平均总价
    area_before = scrapy.Field()          #上月出售平均面积
    add_before = scrapy.Field()           #上月新增出售房源
    rate_mb_unit=scrapy.Field()           #上月较上上月环比(上升或下降)
    rate_mb=scrapy.Field()                #上月较上上月环比

    #新楼盘
    price_new=scrapy.Field()             #平均单价
    rate_new_unit=scrapy.Field()         #同比去年同期（上升或下降）
    rate_new=scrapy.Field()              #同比去年同期

    building=scrapy.Field()              #二手房或新楼盘
    belong=scrapy.Field()                #市或区县房屋信息
    ProgramStarttime=scrapy.Field()       #爬取时间
