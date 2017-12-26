import scrapy
from bs4 import BeautifulSoup
from cityhouse.items import CityhouseItem
import re

class chspider(scrapy.Spider):
    name="cityhouse_city"
    allowed_domains=["cityhouse.cn"]
    start_urls=[
        'http://www.cityhouse.cn/city.html'   #城市房产-全国城市
    ]

    def parse(self, response):
        item=CityhouseItem()
        sel = scrapy.Selector(response)
        webs_info=sel.xpath(".//div[@class='col_detail']/table[@class='table_city']")
        province_info=webs_info.xpath(".//span[contains(@class,'s_province s_plast ordinary_province')]/text()").extract()
        # province_info.insert(19,"山东")
        print(len(province_info))
        print(province_info)
        web_info = webs_info.xpath(".//span[@class='wraplist']")
        print(len(web_info))
        for i in range(len(web_info)):
            item['province']=province_info[i]
            w=web_info[i]
            wraps=w.xpath(".//span[@class='wrap']")
            for wrap in wraps:
                item['city']=wrap.xpath(".//span[@class='m_d_zx']/a/text()").extract()[0]
                city_href=wrap.xpath(".//span[@class='m_d_zx']/a/@href").extract()[0]
                item['city_href']=city_href
                city_web=city_href+'/market/'
                # yield scrapy.Request(url=city_web,callback=self.city,meta=item,dont_filter=True)
                county_list=wrap.xpath(".//span[@class='m_d_city mb5']/a/text()").extract()
                county_href_list=wrap.xpath(".//span[@class='m_d_city mb5']/a/@href").extract()
                for j in range(len(county_list)):
                    item['county']=county_list[j]
                    county_href=county_href_list[j]
                    item['county_href']=county_href
                    yield item
                    # yield scrapy.Request(url=county_href, callback=self.county, meta=item, dont_filter=True)

        zhixiashi_list=webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_zx']/a/text()").extract()
        zhixianshi_href_list=webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_zx']/a/@href").extract()
        zxs_county=webs_info.xpath(".//td[@class='right_city']/span[@class='m_d_city mb5']")
        print(len(zxs_county))
        item['province']=None
        for i in range(len(zxs_county)):
            item['city']=zhixiashi_list[i]
            item['city_href']=zhixianshi_href_list[i]
            z=zxs_county[i]
            county=z.xpath(".//a/text()").extract()
            county_href=z.xpath(".//a/@href").extract()
            for j in range(len(county)):
                item['county']=county[j]
                item['county_href']=county_href[j]
                yield item

    def city(self,response):
        body=response.body
        soup=BeautifulSoup(body,'lxml')




    # def county(self,response):