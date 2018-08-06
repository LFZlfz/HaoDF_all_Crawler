# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HaodfAllCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #以下添加要爬取字段
    #weblist = scrapy.Field()
    title = scrapy.Field()
    disease = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    question_time = scrapy.Field()
    question_cf = scrapy.Field()
    patient_duration = scrapy.Field()
    #patient_history = scrapy.Field()
    #patient_needs = scrapy.Field()
    #patient_location = scrapy.Field()
    patient_name = scrapy.Field()
    doctor_name = scrapy.Field()
    doctor_cbt = scrapy.Field()
    doctor_department = scrapy.Field()
    doctor_adepts = scrapy.Field()
    doctor_answers = scrapy.Field()
