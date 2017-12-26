from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re

# driver = webdriver.Chrome("/home/260199/chrome/chromedriver")
# driver.get("http://www.91my.net/cj/lp/?c=bj")
#
# # 搜索
# info=driver.find_element_by_id("tb1")
# print (info)
# # driver.find_element_by_id("su").click()
# # time.sleep(3)
# driver.close()

# url="http://lz.cityhouse.cn/market/#cityrank"
url="http://zhuhai.qfang.com/fangjia/getTransactionReports?currentPage=1&pageSize=100&currentAreaLevel=cityLevel&currentAreaInternalId=IUthTuDRRnu64%2FkjyZeC9MznrtQ%3D"
x=requests.get(url).text
s = BeautifulSoup(x, 'lxml')
print(s)
page=s.find_all('a')[-2].text
print(page)
info=s.find_all('li',class_='cons clearfix')
# re.findall("")
for inf in info[:2]:
    inf=str(inf)
    print(inf)
    room=re.findall('<em class="rooms">(.*?)</em>',inf)[0]
    print(room)
    louceng=re.findall('<em>(.*?)\r',inf)[0].strip('\t')
    print(louceng)
    location=re.findall('<em>(.*?)</em>',inf)[0]
    print(location)
    area=re.findall('<p class="the-second">(.*?)</p>',inf)[0]
    print(area)
    data=re.findall('<p class="the-third">(.*?)</p>',inf)[0]
    print(room)
    total_price=re.findall('<p class="the-fourth">(.*?)</p>',inf)[0]
    print(total_price)
    price=re.findall('<p class="the-fifth">(.*?)</p>',inf)[0]
    print(price)
    source=re.findall('<p class="the-sixth">(.*?)</p>',inf)[0]
    print(source)
