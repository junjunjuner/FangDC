from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import datetime
import re
import time
# url = "http://www.baidu.com"
# url='http://www.cityhouse.cn/default/forsalerank.html'

#header

# req = requests.get(url)
# print(req.text)
# urls=requests.get(url).text
# s=BeautifulSoup(urls,'lxml')
# print(s)

# driver = webdriver.Chrome("/home/260199/chrome/chromedriver")
# driver.get("http://lz.cityhouse.cn/")
#
# # 搜索
# info=driver.page_source
# print (info)
# # driver.find_element_by_id("su").click()
# # time.sleep(3)
# driver.close()
# one=['ss']
# one=str(one)
# print(one)
now = datetime.datetime.now()
print(now)
x=now.year
print(x)
y=now.month
print(y)
z=str(now.year)+'.'+str(now.month-3)+'月--'+str(now.year)+'.'+str(now.month-1)+'月'
print(z)

first_day = datetime.date(now.year, now.month,1)
first_day=re.sub('-','.',str(first_day))
print(first_day)
x='++'

y=re.sub('1','yi',x)
y=re.sub('-','jian',y)
print(y)

first_day = time.strftime('%Y.%m.1', time.localtime(time.time()))
print(first_day)
last_day = time.strftime('%Y.%m.%d', time.localtime(time.time()))
print(last_day)
date_last=first_day+'--'+last_day
print(date_last)