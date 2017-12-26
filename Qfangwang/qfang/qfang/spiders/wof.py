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
    name="wof"
    allowed_domains=["cityhouse.cn"]
    start_urls=[
        "http://www.cityhouse.cn/default/forsalerank.html"
    ]

    def parse(self, response):
        urls=response.body
        s=BeautifulSoup(urls,'lxml')
        print(s)



