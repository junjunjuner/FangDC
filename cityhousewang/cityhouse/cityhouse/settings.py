# -*- coding: utf-8 -*-

BOT_NAME = 'cityhouse'

SPIDER_MODULES = ['cityhouse.spiders']
NEWSPIDER_MODULE = 'cityhouse.spiders'

ch_user_agent=[
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
#    'gome.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'cityhouse.middlewares.chUseragentMiddleware': 400,
}

ITEM_PIPELINES = {
    'cityhouse.pipelines.CityhousePipeline1': 300,
    'cityhouse.pipelines.CityhousePipeline2': 300,
    'cityhouse.pipelines.CSVPipeline1': 200,
    'cityhouse.pipelines.CSVPipeline2': 200
}

FIELDS_TO_EXPORT1 = [
    'province' , # 省
    'city', # 市
    'city_href',   # 市链接
    'county'  ,# 区县
    'county_href' , # 区县链接
    'date_range'  , # 上三个月
    'number'  , # 出售数量
    'value',  # 市场价值
    'date_last',  # 近一个月
    'price_last',  # 近一月平均单价
    'rate_ml_unit',
    'rate_ml' ,# 环比上月
    'add_last' ,# 近一月新增出售房源
    'date_before',  # 上一个月
    'rate_y_unit',
    'rate_y', # 同比去年
    'price_before' , # 上月出售平均单价
    'totalprice_before' , # 上月出售平均总价
    'area_before',   # 上月出售平均面积
    'add_before',  # 上月新增出售房源
    'rate_mb_unit',
    'rate_mb',      #上月较上上月环比
    'belong',       #市或区县信息
    'building',
    'ProgramStarttime'   #爬取时间
]

FIELDS_TO_EXPORT2 = [
    'province' , # 省
    'city', # 市
    'city_href',   # 市链接
    'county'  ,# 区县
    'county_href' , # 区县链接
    'date_before',
    'rate_new_unit',
    'rate_new',
    'price_new',
    'belong',       #市或区县信息
    'building',
    'ProgramStarttime'   #爬取时间
]

# MONGO_HOST = "172.28.163.228"  # 主机IP
MONGO_HOST = "172.28.171.13"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "FangDC"  # 库名
MONGO_COLL1 = "cityhouse_city_old"  # 文档(相当于关系型数据库的表名)
MONGO_COLL2 = "cityhouse_city_new"
# LOG_FILE='jd取暖器_log_%s.txt' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
LOG_FILE='cityhouse_log.txt'

