import scrapy
from bs4 import BeautifulSoup
import requests
import re
from qfang.items import QfangItem
import pandas as pd
import pypinyin  # python汉字转拼音库
from pypinyin import pinyin, lazy_pinyin
import json
import time,random

class qfang(scrapy.Spider):
    name="qfang"
    allowed_domains=["qfang.com"]
    start_urls=[
        "https://beijing.qfang.com/deal"
    ]

    def parse(self, response):
        item=QfangItem()
        df = pd.read_excel("城市列表及ID.xlsx")
        city = df['二级'].drop_duplicates()
        print(city)
        for c in city:
            city_pinyin = ''.join(lazy_pinyin(c))
            print(city_pinyin)
            url = "http://"+str(city_pinyin)+".qfang.com/fangjia/getTransactionReports?currentPage=1&pageSize=100&currentAreaLevel=cityLevel&currentAreaInternalId=IUthTuDRRnu64%2FkjyZeC9MznrtQ%3D"
            try:
                x = requests.get(url).text
                s = BeautifulSoup(x, 'lxml')
                page = s.find_all('a')[-2].text
                print(page)
                i=1
                while i<=int(page):
                    print(i)
                    url = "http://"+str(city_pinyin)+".qfang.com/fangjia/getTransactionReports?currentPage="+str(i)+"&pageSize=100&currentAreaLevel=cityLevel&currentAreaInternalId=IUthTuDRRnu64%2FkjyZeC9MznrtQ%3D"
                    urls = requests.get(url).text
                    s = BeautifulSoup(urls, 'lxml')
                    info = s.find_all('li', class_='cons clearfix')
                    for inf in info:
                        inf = str(inf)
                        room = re.findall('<em class="rooms">(.*?)</em>', inf)[0]
                        # print(room)
                        floor = re.findall('<em>(.*?)\r', inf)[0].strip('\t')
                        # print(louceng)
                        location = re.findall('<em>(.*?)</em>', inf)[0]
                        # print(location)
                        area = re.findall('<p class="the-second">(.*?)</p>', inf)[0]
                        # print(area)
                        date = re.findall('<p class="the-third">(.*?)</p>', inf)[0]
                        # print(room)
                        total_price = re.findall('<p class="the-fourth">(.*?)</p>', inf)[0]
                        # print(total_price)
                        price = re.findall('<p class="the-fifth">(.*?)</p>', inf)[0]
                        # print(price)
                        source = re.findall('<p class="the-sixth">(.*?)</p>', inf)[0]
                        print(room,floor,location,area,date,total_price,price,source)
                        item['city_pinyin']=city_pinyin
                        item['city']=c
                        item['room']=room
                        item['floor']=floor
                        item['location']=location
                        item['area']=area
                        item['date']=date
                        item['total_price']=total_price
                        item['price']=price
                        item['source']=source
                        yield item
                    i = i + 1
            except:
                item['city_pinyin'] = city_pinyin
                item['city'] = c
                item['room'] = None
                item['floor'] = None
                item['location'] = None
                item['area'] = None
                item['date'] = None
                item['total_price'] = None
                item['price'] = None
                item['source'] = None
                yield item




