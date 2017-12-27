# -*- coding: utf-8 -*-

# Scrapy settings for house project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'house'

SPIDER_MODULES = ['house.spiders']
NEWSPIDER_MODULE = 'house.spiders'

house_user_agent=[
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

RETRY_ENABLED=True
RETRY_TIMES=5                #重试次数

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'house.middlewares.houseUseragentMiddleware': 400,
}

ITEM_PIPELINES = {
    'house.pipelines.HousePipeline1': 300,
    'house.pipelines.HousePipeline2': 300,
    'house.pipelines.CSVPipeline1': 200,
    'house.pipelines.CSVPipeline2': 200
}

FIELDS_TO_EXPORT1 = [
    'province' , # 省
    'city', # 市
    'city_href',   # 市链接
    'county'  ,# 区县
    'county_href' , # 区县链接
    'oldhome_href', #获取二手房小区信息的链接
    'house',        #小区名称
    'date_before',
    'price',        #房价
    'rate_m_unit',
    'rate_m',       #环比上月
    'building',       #二手房或新楼盘
    'ProgramStarttime'   #爬取时间
]
FIELDS_TO_EXPORT2 = [
    'province' , # 省
    'city', # 市
    'city_href',   # 市链接
    'county'  ,# 区县
    'county_href' , # 区县链接
    'newhome_href', #获取新楼盘小区信息的链接
    'house',        #小区名称
    'price_type',   #房价类型
    'price',        #房价
    'time',        #房价更新时间
    'date_before',  #上月
    'building',       #二手房或新楼盘
    'ProgramStarttime'   #爬取时间
]

# MONGO_HOST = "172.28.163.228"  # 主机IP
MONGO_HOST = "172.28.171.13"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "FangDC"  # 库名
MONGO_COLL1 = "cityhouse_house_old"  # 文档(相当于关系型数据库的表名)
MONGO_COLL2 = "cityhouse_house_new"
# LOG_FILE='jd取暖器_log_%s.txt' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
# LOG_FILE='house_log.txt'
