import scrapy
from bs4 import BeautifulSoup
from cityhouse.items import CityhouseItem
import re
import time
import requests
import datetime


class chspider(scrapy.Spider):
    name = "cityhouse"
    allowed_domains = ["cityhouse.cn"]
    start_urls = [
        'http://www.cityhouse.cn/city.html'  # 城市房产-全国城市
    ]
    ProgramStarttime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = datetime.datetime.now()
    date_range= str(now.year) + '.' + str(now.month - 3) + '月--' + str(now.year) + '.' + str(now.month - 1)+'月'
    date_before=str(now.year) + '.' + str(now.month - 1)+'月'
    first_time=time.strftime('%Y.%m.1', time.localtime(time.time()))
    last_time=time.strftime('%Y.%m.%d', time.localtime(time.time()))

    def parse(self, response):
        item = CityhouseItem()
        sel = scrapy.Selector(response)
        webs_info = sel.xpath(".//div[@class='col_detail']/table[@class='table_city']")
        #获得省名称（27个省的列表）
        #山东class='s_province s_plast ordinary_province '多了个空格，其他省最后无空格，只能用包含判断
        province_info = webs_info.xpath(".//span[contains(@class,'s_province s_plast ordinary_province')]/text()").extract()
        # province_info.insert(19,"山东")
        web_info = webs_info.xpath(".//span[@class='wraplist']")
        #将每个省分开分析
        for i in range(len(web_info)):
            #获得各省名称
            item['province'] = province_info[i]
            w = web_info[i]
            #获得各省对应所有市的信息
            wraps = w.xpath(".//span[@class='wrap']")
            #将各市分开分析
            for wrap in wraps:
                #获得每个市的名称
                item['city'] = wrap.xpath(".//span[@class='m_d_zx']/a/text()").extract()[0]
                #获得每个市的链接
                city_href = wrap.xpath(".//span[@class='m_d_zx']/a/@href").extract()[0]
                item['city_href'] = city_href
                #将区县及其链接置空是为了与区县信息一致（表头一致）
                item['county'] = None
                item['county_href'] = None
                #市信息没有上月与上上月环比比较
                item['rate_mb_unit'] = None
                item['rate_mb'] = None
                item['belong']="市房屋信息"
                #市二手房详细信息链接
                city_web = city_href + '/market/'
                #获得市二手房信息
                yield scrapy.Request(url=city_web, callback=self.city_county, meta=item, dont_filter=True)
                # 市新楼盘详细信息链接
                city_new_web = city_href + '/newhamarket/'
                # 获得市新楼盘信息
                yield scrapy.Request(url=city_new_web, callback=self.city_county_new, meta=item, dont_filter=True)
                #市对应各区县房价涨幅链接
                city_county=city_href+'/market/rankforsale.html'
                #获得区县详细信息链接
                yield scrapy.Request(url=city_county, callback=self.county, meta=item, dont_filter=True)

        #直辖市列表（没有对应的省）
        zhixiashi_list = webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_zx']/a/text()").extract()
        #直辖市链接列表
        zhixianshi_href_list = webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_zx']/a/@href").extract()
        #直辖市所有区信息
        zxs_county = webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_city mb5']")
        for i in range(len(zxs_county)):
            item['province'] = zhixiashi_list[i]
            #获得每个直辖市的名称
            item['city'] = zhixiashi_list[i]
            #获得每个直辖市的链接
            city_href = zhixianshi_href_list[i]
            item['city_href'] = city_href
            #将区及其链接置空是为了与区信息一致（表头一致）
            item['county'] = None
            item['county_href'] = None
            # 市信息没有上月与上上月环比比较
            item['rate_mb_unit'] = None
            item['rate_mb']=None
            item['belong']="市房屋信息"
            #直辖市二手房详细信息链接
            city_web = city_href + '/market/'
            #获得市二手房信息
            yield scrapy.Request(url=city_web, callback=self.city_county, meta=item, dont_filter=True)
            # 直辖市新楼盘详细信息链接
            city_new_web = city_href + '/newhamarket/'
            # 获得市新楼盘信息
            yield scrapy.Request(url=city_new_web, callback=self.city_county_new, meta=item, dont_filter=True)
            # 市对应各区房价涨幅链接
            city_county = city_href + '/market/rankforsale.html'
            # 获得区详细信息链接
            yield scrapy.Request(url=city_county, callback=self.county, meta=item, dont_filter=True)

        # #测试用(获得详细信息)
        # item['province']=None
        # item['city'] = None
        # # 获得每个市的链接
        # city_href = 'http://df.cityhouse.cn/market/distDF/'
        # item['city_href'] = city_href
        # # 将区县及其链接置空是为了与区县信息一致（表头一致）
        # item['county'] = '东方'
        # item['county_href'] = 'http://df.cityhouse.cn/market/distDF/'
        # # 市信息没有上月与上上月环比比较
        # item['rate_mb_unit'] = None
        # item['rate_mb'] = None
        # item['belong'] = "测试信息"
        # yield scrapy.Request(url=city_href, callback=self.city_county, meta=item, dont_filter=True)
        #
        # #测试用（获得区县信息）
        #     # 'http://huizhou.cityhouse.cn/market/rankforsale.html'
        # item['province']='广东'
        # item['city'] = '惠州'
        # # 获得每个市的链接
        # city_href = 'http://huizhou.cityhouse.cn'
        # item['city_href'] = city_href
        # # 将区县及其链接置空是为了与区县信息一致（表头一致）
        # item['county'] = None
        # item['county_href'] = None
        # # 市信息没有上月与上上月环比比较
        # item['rate_mb'] = None
        # item['belong'] = "测试信息"
        # city_county = city_href + '/market/rankforsale.html'
        # yield scrapy.Request(url=city_county, callback=self.county, meta=item, dont_filter=True)

    #市及区县详细信息（市与区县详细信息页面一致）
    def city_county(self, response):
        # if response.status==
        #从上一函数传下来
        item=response.meta
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        county=item['county']
        county_href=item['county_href']
        rate_mb_unit=item['rate_mb_unit']
        rate_mb=item['rate_mb']
        belong=item['belong']
        url=response.url
        item = CityhouseItem()
        #存储到此函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
        #市为None，区县有数据
        item['county'] = county
        item['county_href'] = county_href
        #市为None，区县有数据
        item['rate_mb_unit']=rate_mb_unit
        item['rate_mb']=rate_mb
        item['belong']=belong
        item['building'] = '二手房'
        item['ProgramStarttime']=self.ProgramStarttime
        body=response.body
        soup=BeautifulSoup(body,"lxml")
        #包含上三个月内容
        three_m=soup.find_all('div',class_='market-title-s')
        # 会出现传入的第一个链接，获取内容不全的情况
        if three_m==[]:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            urls=requests.get(url,headers=headers).text
            soup=BeautifulSoup(urls,'lxml')
            three_m = soup.find_all('div', class_='market-title-s')

        three_m=str(three_m)
        try:
            #获取城市名称
            name=re.findall('<h1 class="tith active">(.*?)房价</h1>',three_m)[0]
        except:
            name=None
        #对比链接是否有错
        if name==city or name==county:
            item['date_range']=self.date_range
            try:
                #数据统计的是该行政区上三个月的在售住宅数量及总价之和
                item['number']=re.findall('<span class="mr5">出售数量：(.*?)</span>',three_m)[0]
                if item['number']=='--套':
                    item['number']='--'
                item['value']=re.findall('<span class="sm">市场价值：(.*?)</span>',three_m)[0]
                if item['value']=='--元':
                    item['value']='--'
            except:
                item['number']=None
                item['value']=None

            #近一个月那一列部分的内容
            one_m=soup.find_all('div',class_='price_boxnl city-price clearfix')
            one_m = str(one_m)
            item['date_last'] = self.first_time+'--'+self.last_time
            try:
                try:
                    #近一月房价单价（单位元/㎡）
                    item['price_last']=''.join(re.findall('<span class="mr5 numg">(.*?)</span><span class="mr wz_c">(.*?)</span>',one_m)[0])
                except:
                    item['price_last'] = ''.join(re.findall('<span class="mr5 numr">(.*?)</span><span class="mr wz_c">(.*?)</span>', one_m)[0])
                if item['price_last'] == '--元/㎡':
                    item['price_last'] = '--'
                # unit_pl=re.findall('<span class="mr wz_c">(.*?)</span>',one_m)          #单价的单位
                # 近一月环比上月（房价实况较上月房价涨跌幅）
                rate_mlinfo=re.findall('<span class="f14 simsun vm">(.*?)</span>(.*?)</span><i class="ask" title="房价实况较上月房价涨跌幅"></i>',one_m)[0]
                rate_ml_unit=re.sub('↑','上升',rate_mlinfo[0])
                rate_ml_unit=re.sub('↓','下降',rate_ml_unit)
                item['rate_ml_unit']=rate_ml_unit
                item['rate_ml']=rate_mlinfo[1]
                item['add_last']=re.findall('<div class="mt">新增房源：(.*?)</div>',one_m)[0]
                # http://cq.cityhouse.cn/market/distWX/
            except:
                item['price_last']=None
                item['rate_ml_unit']=None
                item['rate_ml']=None
                item['add_last']=None

            item['date_before']=self.date_before
            try:
                # 上一个月房价同比去年（同比去年同期）
                rate_yinfo=re.findall('<span class="f14 simsun vm">(.*?)</span><span>(.*?)</span></span>',one_m)[0]
                rate_y_unit=re.sub('↑','上升',rate_yinfo[0])
                rate_y_unit=re.sub('↓','下降',rate_y_unit)
                item['rate_y_unit']=rate_y_unit
                item['rate_y']=rate_yinfo[1]
            except:
                item['rate_y_unit'] = None
                item['rate_y']=None
            #房价走势部分的内容
            one_bm=soup.find_all('div',class_='price_boxnl mb20')
            one_bm=str(one_bm)
            try:
                #上一个月房价平均单价
                item['price_before']=''.join(re.findall('<span class="mr20">平均单价：<span class="red">(.*?)</span>(.*?)</span>',one_bm)[0])
                if item['price_before'] == '--元/㎡':
                    item['price_before'] = '--'
                # unit_pb=price_binfo[1]
                #上一个月出售总价平均总价
                item['totalprice_before']=''.join(re.findall('<span class="mr20">平均总价：<span class="red">(.*?)</span>(.*?)</span>',one_bm)[0])
                #上一个月出售户型平均面积(单位：㎡)
                item['area_before']=''.join(re.findall('<span class="mr20">平均面积：<span class="red">(.*?)</span>(.*?)</span>',one_bm)[0])
                #上一个月供给新增房源
                item['add_before']=''.join(re.findall('<span class="mr20">新增房源：<span class="red">(.*?)</span>(.*?)</span>',one_bm)[0])
            except:
                item['price_before']=None
                item['totalprice_before']=None
                item['area_before']=None
                item['add_before']=None
            yield item
        else:
            if name==None:
                print("url:",url)
            else:
                print("city与传入不符:",name,city,county)

    #获得区县链接
    def county(self,response):
        item=response.meta
        #继承上个函数得到省市及链接
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        url=response.url
        item = CityhouseItem()
        #存储到该函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
        item['belong']="区县房屋信息"
        body=response.body
        soup=BeautifulSoup(body,"lxml")
        tbody=soup.find_all('tbody',class_=None)
        # 会出现传入的第一个链接，获取内容不全的情况
        if tbody==[]:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            urls=requests.get(url,headers=headers).text
            soup=BeautifulSoup(urls,'lxml')
            tbody = soup.find_all('tbody', class_=None)
        #包含一个市的所有区县信息
        tr=tbody[-1].find_all('tr',class_=None)
        #获得每个区县信息
        for t in tr[1:]:
            t=str(t).replace('\n','').replace('\r','').replace('\t','')
            # print(t)
            try:
                county_info=re.findall('<a class="c_blue" href="(.*?)" title="(.*?)">(.*?)</a>',t)[0]
                #获得区县名称
                item['county']=county_info[-1]
                #获得区县详细信息链接
                county_href=city_href+county_info[0]
                item['county_href']=county_href
            except:
                county_info = re.findall('<a title="(.*?)" href="(.*?)" class="c_blue">(.*?)</a>', t)[0]
                item['county']=county_info[-1]
                county_href=city_href+county_info[1]
                item['county_href']=county_href
            try:
                #获得一个区县上个月较上上个月环比比较信息
                rate_mb=re.findall('<td class="c_green2">(.*?)</td><td',t)[0]
            except:
                try:
                    rate_mb= re.findall('<td class="c_red">(.*?)</td><td', t)[0]
                except:
                    rate_mb = re.findall('<td class="">(.*?)</td><td', t)[0]
            if '%' in rate_mb:
                rate_mb=re.sub('-','下降',rate_mb)
                rate_mb = re.sub('\+', '上升', rate_mb)
            if '下降' in rate_mb:
                item['rate_mb_unit']='下降'
                item['rate_mb'] =rate_mb.replace('下降','')
            elif '上升' in rate_mb:
                item['rate_mb_unit'] = '上升'
                item['rate_mb'] = rate_mb.replace('上升', '')
            else:
                item['rate_mb_unit']=None
                item['rate_mb'] =rate_mb
            yield scrapy.Request(url=county_href, callback=self.city_county, meta=item, dont_filter=True)
            #获得区县新楼盘链接
            county_new_href=county_href.replace('/market/','/newhamarket/')
            item['county_href'] = county_new_href
            yield scrapy.Request(url=county_new_href, callback=self.city_county_new, meta=item, dont_filter=True)

    #获取市区县新楼盘信息
    def city_county_new(self,response):
        #从上一函数传下来
        item=response.meta
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        county=item['county']
        county_href=item['county_href']
        belong=item['belong']
        url=response.url
        item = CityhouseItem()
        #存储到此函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
        #市为None，区县有数据
        item['county'] = county
        item['county_href'] = county_href
        item['belong']=belong
        item['building']='新楼盘'
        item['date_before']=self.date_before
        item['ProgramStarttime']=self.ProgramStarttime
        body=response.body
        soup=BeautifulSoup(body,"lxml")
        #近一月那一列
        box=soup.find_all('div',class_='p_nrbox')
        if box==[]:   #会出现获取信息不全的情况
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            urls=requests.get(url,headers=headers).text
            soup=BeautifulSoup(urls,'lxml')
            box = soup.find_all('div', class_='p_nrbox')
        box = str(box).replace('\n', '').replace('\r', '').replace('\t', '')
        #新楼盘上一月均价
        try:
            item['price_new']=''.join(re.findall('<span class="mr5 numr">(.*?)</span><span class="mr wz_c">(.*?)</span>',box)[0])
            if item['price_new']=='--元/㎡':
                item['price_new']='--'
            #同比去年同期
            rate_new=re.findall('<span class="f14 simsun vm">(.*?)</span>(.*?)</span><i class="ask" title="同比去年同期">',box)[0]
            if rate_new[0]=='↑':
                item['rate_new_unit']='上升'
            elif rate_new[0]=='↓':
                item['rate_new_unit'] = '下降'
            else:
                item['rate_new_unit']=rate_new[0]
            item['rate_new']=rate_new[1].strip()
        except:
            item['price_new']=None
            item['rate_new_unit']=None
            item['rate_new']=None
        yield item