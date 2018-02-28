# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    job_request = scrapy.Field()
    job_position = scrapy.Field()
    job_advantage = scrapy.Field()
    job_description = scrapy.Field()
    job_address = scrapy.Field()


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    domain = scrapy.Field()
    stage = scrapy.Field()
    scale = scrapy.Field()
    home_page = scrapy.Field()
