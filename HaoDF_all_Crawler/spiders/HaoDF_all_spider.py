# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml.html import etree

from HaoDF_all_Crawler.items import  HaodfAllCrawlerItem
from symbol import except_clause

class HaodfAllSpiderSpider(scrapy.Spider):
    name = 'HaoDF_all_spider'
    allowed_domains = ['zixun.haodf.com']
    start_urls = ['http://zixun.haodf.com/']

    def parse(self, response):
        #weblist = response.xpath("//div[@class='map_all']/div[@class='dis_article_2 clearfix']/li[@class='hh']").extract()

        title = response.xpath("//div[@class='h_s_info_cons']/h3[@class='h_s_cons_info_title']/text()").extract()

        disease = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/h2/a/text()").extract_first()
        if disease == None :
            disease = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/h2/text()").extract()[0]

        question_time = response.xpath("//div[@class='stream_yh_left'] /div[@class='yh_l_times']/text()").extract()[0]
        question_cf = response.xpath("//div[@class='zzx_yh_con clearfix'] /div[@class='stream_left_content fl']/div[@class='pb20']/div[@class='ask-width ask-headmap']/a/text()").extract()

        patient_duration = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/h2/text()").extract()[1]
        #patient_history = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/h2/text()").extract()[2]
        #patient_needs = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/p/text()").extract()[8]
        #patient_location = response.xpath("//div[@class='stream_yh_right'] /div[@class='h_s_cons_info']/div[@class='h_s_info_cons']/p/text()").extract()[11]
        patient_name = response.xpath("//div[@class='stream_yh_left'] /div[@class='yh_l_huan']/text()").extract()[0]

        doctor_name = response.xpath("//div[@class='space_b_doc_con clearfix'] /div[@class='space_b_picright']/div[@class='doc_title clearfix']/h3[@class='doc_name f22 fl']/text()").extract()
        doctor_cbt = response.xpath("//div[@class='right_content fr'] /div[@class='mr_line1 mb20']/ul[@class='doc_info_ul1']/li[3]/span/a/text()").extract()
        doctor_department = response.xpath("//div[@class='right_content fr'] /div[@class='mr_line1 mb20']/div[@class='fs pr15 pb10 pl15']/div[@class='clearfix pt5 bb_d pb5']/div[@class='hh']/a/text()").extract()
        doctor_adepts = response.xpath("//div[@class='right_content fr'] /div[@class='mr_line1 mb20']/div[@class='fs pr15 pb10 pl15']/div[@class='clearfix pt5 bb_d pb5']/div[@class='hh']/text()").extract()[2]
        doctor_answers = response.xpath("//div[@class='zzx_yh_stream'] /div[@class='stream_yh_right']/div[@class='h_s_cons_docs']/h3[@class='h_s_cons_title']/text()").extract()

        des = response.xpath("//div[@class='h_s_info_cons']/div[1]/strong[1]/text()").extract_first()
        if "病情描述" in des:
            descriptions = response.xpath("//div[@class='h_s_info_cons']/div[1]/text()").extract()
            description = " ".join([x.strip() for x in descriptions if x])

        #以上14项
        item = HaodfAllCrawlerItem()
        # item["weblist"] = weblist
        item["title"] = title
        item["disease"] = disease
        item["description"] = description
        item["url"] = response.url
        item["question_time"] =question_time
        item["question_cf"] = question_cf
        item["patient_duration"] = patient_duration
        #item["patient_history"] = patient_history
        #item["patient_needs"] = patient_needs
        #item["patient_location"] = patient_location
        item["patient_name"] = patient_name
        item["doctor_name"] = doctor_name
        item["doctor_cbt"] = doctor_cbt
        item["doctor_department"] = doctor_department
        item["doctor_adepts"] = doctor_adepts
        item["doctor_answers"] = doctor_answers


        yield item


    def start_requests(self):
        header_data = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Host": "www.haodf.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }

        #'12', '11', '10', '09', '08',
        x = '2018'
        for y in ['07','06','05','04','03','02','01']:
            for z in ['31','30','29','28','27','26','25','24','23','22','21','20','19','18','17','16','15','14','13','12','11','10','09','08','07','06','05','04','03','02','01']:
                for p in range(21):
                    if p != 0 :
                        cur_url = 'https://www.haodf.com/sitemap-zx/' + x + y + z + '_' + str(p) + '/'

                        #print(cur_url)

                        res = requests.get(cur_url, headers=header_data)
                        html_con = etree.HTML(res.content)
                            #判断网页是否有效
                        if html_con.xpath("//div[@class='map_all']/text()") == '\n' :
                           break

                        urls = html_con.xpath("//div[@class='map_all']/div[@class='dis_article_2 clearfix']/li[@class='hh']/a/@href")  # 获取爬取页面地址
                        for url in urls:  # 遍历爬取页面
                            #print(url)
                            yield scrapy.Request("https:" + url, callback=self.parse)
                        #yield scrapy.Request(cur_url, callback=self.parse)
'''

            #//表示相对路径   /表示绝对路径   @表示属性   text()表示内容
            
            urls = html_con.xpath("//li[@class='clearfix']/span[@class='fl']/a[2]/@href")#获取终端爬取页面地址
            for url in urls:                                                             #遍历爬取页面
                yield scrapy.Request("https:" + url, callback=self.parse)
                
                scrapy crawl HaoDF_all_spider -o res.jl/res.json/res.csv
                scrapy crawl HaoDF_all_spider -o weblist.jl -s FEED_EXPORT_ENCODING=utf-8
'''


