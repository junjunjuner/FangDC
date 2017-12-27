import scrapy
from bs4 import BeautifulSoup
from house.items import HouseItem
from lxml.etree import HTML
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
        item = HouseItem()
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
            # 市对应各区房价涨幅链接
            city_county = city_href + '/market/rankforsale.html'
            # 获得区详细信息链接
            yield scrapy.Request(url=city_county, callback=self.county, meta=item, dont_filter=True)

        # #测试用(获得详细信息)
        # item['province']=None
        # item['city'] = None
        # # 获得每个市的链接
        # city_href = 'http://dx.cityhouse.cn/ha/dsZX/'
        # item['city_href'] = city_href
        # # 将区县及其链接置空是为了与区县信息一致（表头一致）
        # item['county'] = None
        # item['county_href'] = city_href
        # item['newhome_fweb']=city_href
        # item['newhome_href']=city_href
        # item['cpage']=1
        # # 市信息没有上月与上上月环比比较
        # yield scrapy.Request(url=city_href, callback=self.newhome, meta=item, dont_filter=True)

    #获得区县对应小区链接
    def county(self,response):
        item=response.meta
        #继承上个函数得到省市及链接
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        url=response.url
        item = HouseItem()
        #存储到该函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
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
                #获取区县小区链接
                oldhome_href=county_href[:-1].replace('/market/dist','/ha/list/salesort.html?dist=')
                item['county_href']=county_href
                item['oldhome_href']=oldhome_href
            except:
                county_info = re.findall('<a title="(.*?)" href="(.*?)" class="c_blue">(.*?)</a>', t)[0]
                item['county']=county_info[-1]
                county_href=city_href+county_info[1]
                #获得区县小区二手房链接
                oldhome_href=county_href[:-1].replace('/market/dist','/ha/list/salesort.html?dist=')
                item['county_href']=county_href
                item['oldhome_href']=oldhome_href
            #转到小区二手房信息
            yield scrapy.Request(url=oldhome_href, callback=self.oldhome, meta=item, dont_filter=True)
            #获得区县小区新楼盘链接
            newhome_href=county_href.replace('/market/dist','/ha/ds')
            item['cpage']=1
            item['newhome_href'] = newhome_href
            #区县小区首页链接（中间变量）
            item['newhome_fweb']=newhome_href
            #转到小区新楼盘信息
            yield scrapy.Request(url=newhome_href, callback=self.newhome, meta=item, dont_filter=True)

    #小区二手房信息
    def oldhome(self, response):
        # if response.status==
        sel=scrapy.Selector(response)
        #从上一函数传下来
        item=response.meta
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        county=item['county']
        county_href=item['county_href']
        oldhome_href=item['oldhome_href']
        url=response.url
        item = HouseItem()
        #存储到此函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
        item['county'] = county
        item['county_href'] = county_href
        item['oldhome_href']=oldhome_href
        item['date_before']=self.date_before
        item['building'] = '二手房'
        item['ProgramStarttime']=self.ProgramStarttime
        # 有小区信息那一部分
        detail_table=sel.xpath(".//div[@class='l-c']/div[@class='gary-detail pdd-5']/table[@class='ha_detail_table mt']")
        # 会出现传入的第一个链接，获取内容不全的情况
        #xpath重新获取时，HTML不能用extract(),所以后续不能合并处理
        if detail_table==[]:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            urls=requests.get(url,headers=headers).text
            html=HTML(urls)
            #有该页小区信息那一部分
            detail_table = html.xpath(".//div[@class='l-c']/div[@class='gary-detail pdd-5']/table[@class='ha_detail_table mt']")[0]
            #该区县所有小区列表
            detail=detail_table.xpath(".//tr[@height='25px;']")
            #获取各个小区信息
            for d in detail:
                #小区名称
                item['house']=d.xpath(".//a[@class='c_blue']/text()")[0]
                #上月房价（平均单价）
                item['price']=d.xpath(".//td[4]/span/text()")[0]
                #环比上月信息
                rate=d.xpath(".//td[5]/span/text()")[0]
                if '--' not in rate:
                    if rate[0]=='-':
                        item['rate_m_unit']='下降'
                        item['rate_m'] = rate[1:]
                    elif rate[0]=='+':
                        item['rate_m_unit']='上升'
                        item['rate_m'] = rate[1:]
                    else:
                        item['rate_m_unit']=None
                        item['rate_m'] = rate
                else:
                    item['rate_m_unit'] = None
                    item['rate_m'] = rate
                yield item
        else:
            # 该区县所有小区列表
            detail=detail_table.xpath(".//tr[@height='25px;']")
            # 获取各个小区信息
            for d in detail:
                # 小区名称
                item['house'] = d.xpath(".//a[@class='c_blue']/text()").extract()[0]
                # 上月房价（平均单价）
                item['price'] = d.xpath(".//td[4]/span/text()").extract()[0]
                # 环比上月信息
                rate = d.xpath(".//td[5]/span/text()").extract()[0]
                if '--' not in rate:
                    if rate[0] == '-':
                        item['rate_m_unit'] = '下降'
                        item['rate_m'] = rate[1:]
                    elif rate[0] == '+':
                        item['rate_m_unit'] = '上升'
                        item['rate_m'] = rate[1:]
                    else:
                        item['rate_m_unit'] = None
                        item['rate_m'] = rate
                else:
                    item['rate_m_unit'] = None
                    item['rate_m'] = rate
                yield item

    #小区新楼盘信息
    def newhome(self,response):
        #从上一函数传下来
        sel=scrapy.Selector(response)
        item=response.meta
        province=item['province']
        city=item['city']
        city_href=item['city_href']
        county=item['county']
        # 中间变量（不返回到yield item）
        cpage=item['cpage']         #当前页
        county_href=item['county_href']
        newhome_href = item['newhome_href']
        # 中间变量（不返回到yield item）
        newhome_fweb=item['newhome_fweb']    #首页链接（为了后续拼翻页链接）
        url=response.url
        item = HouseItem()
        #存储到此函数
        item['province'] = province
        item['city'] = city
        item['city_href'] = city_href
        item['county'] = county
        item['county_href'] = county_href
        item['newhome_href']=newhome_href
        item['building']='新楼盘'
        item['date_before']=self.date_before
        item['ProgramStarttime']=self.ProgramStarttime
        boxs=sel.xpath(".//div[@id='content']/div[@class='halistbox']")
        # xpath重新获取时，HTML不能用extract(),所以后续不能合并处理
        if boxs==[]:   #会出现获取信息不全的情况
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            urls=requests.get(url,headers=headers).text
            html = HTML(urls)
            #有该页所有小区信息那一部分
            boxs = html.xpath(".//div[@id='content']/div[@class='halistbox']")[0]
            #小区信息列表
            box=boxs.xpath(".//div[@class='halist clearfix']")
            #各个小区
            for b in box:
                #小区名称
                item['house']=b.xpath(".//div[@class='title mb5 clearfix']/h4[@class='tit fl mr']/a/text()")[0]
                #text=['均价：', '元/㎡', '(2017-06-12)'] 或[]
                text=b.xpath(".//div[@class='text']/ul[@class='mb15']/li[1]/*/text()")
                if text:
                    try:  #房价类型
                        item['price_type']=text[0][:-1]
                    except:
                        item['price_type']=None
                    try:   #房价发布时间
                        item['time']=text[2][1:-1]
                    except:
                        item['time']=None
                #price_info=['25,000']或[]
                price_info=b.xpath(".//div[@class='text']/ul[@class='mb15']/li[1]/span/*/text()")
                if price_info:   #房价
                    item['price']=price_info[0]
                    yield item
            #共**页
            try:
                pages=boxs.xpath(".//div[@class='page1 mb5 clearfix']/span[@class='page_p']/text()")[0]
                page=int(re.findall("共(.*?)页",pages)[0])
            except:
                page=None
        else:
            #小区信息列表
            box=boxs.xpath(".//div[@class='halist clearfix']")
            #各个小区
            for b in box:
                #小区名称
                item['house']=b.xpath(".//div[@class='title mb5 clearfix']/h4[@class='tit fl mr']/a/text()").extract()[0]
                #text=['均价：', '元/㎡', '(2017-06-12)'] 或[]
                text=b.xpath(".//div[@class='text']/ul[@class='mb15']/li[1]/*/text()").extract()
                if text:
                    try:
                        #房价类型（均价或起价）
                        item['price_type']=text[0][:-1]
                    except:
                        item['price_type']=None
                    try:  #房价更新时间
                        item['time']=text[2][1:-1]
                    except:
                        item['time']=None
                # price_info=['25,000']或[]
                price_info=b.xpath(".//div[@class='text']/ul[@class='mb15']/li[1]/span/*/text()").extract()
                if price_info:
                    item['price']=price_info[0]
                    yield item
            # 共**页
            try:
                pages=boxs.xpath(".//div[@class='page1 mb5 clearfix']/span/text()").extract()[0]
                page=int(re.findall("共(.*?)页",pages)[0])
            except:
                page=None

        #翻页
        if page:
            if cpage<page:
                #根据各区县小区首页链接拼翻页链接
                newhome_href=newhome_fweb[:-1]+"-pg"+str(cpage+1)+"/"
                item['cpage']=cpage+1
                item['newhome_fweb']=newhome_fweb
                item['newhome_href']=newhome_href
                yield scrapy.Request(url=newhome_href, callback=self.newhome, meta=item, dont_filter=True)
