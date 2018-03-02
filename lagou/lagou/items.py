# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    link_url = scrapy.Field()
    job_tilte = scrapy.Field()
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    job_request = scrapy.Field()
    job_position = scrapy.Field()
    job_advantage = scrapy.Field()
    job_description = scrapy.Field()
    job_positionLng = scrapy.Field()
    job_positionLat = scrapy.Field()
    job_positionAddress = scrapy.Field()
    job_workAddress = scrapy.Field()
    company_name = scrapy.Field()
    company_domain = scrapy.Field()
    company_stage = scrapy.Field()
    company_scale = scrapy.Field()
    company_home_page = scrapy.Field()
