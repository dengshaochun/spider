#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/28 19:57
# @Author  : Dengsc
# @Site    : 
# @File    : lagou_spider.py
# @Software: PyCharm


from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from ..items import JobsItem, CompanyItem


class DmozSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = [
        'https://www.lagou.com/'
    ]

    rules = [
        Rule(sle(allow=('/jobs/[0-9]+.html$')), callback='parse_jobs', follow=True),
    ]

    def parse_job_page(self, response, ):
        job_obj = JobsItem()
        comp_obj = CompanyItem()
        selector = Selector(response)
        job_obj.company_name = selector.xpath('//div[@class="company"]/text()')
        job_obj.job_name = selector.xpath('//span[@class="name"]/text()')
        job_obj.salary = selector.xpath('//span[@class="salary"]/text()')
        job_obj.job_advantage = selector.xpath('//dd[@class="job-advantage"]/p/text()')
        job_obj.job_description = []
        job_obj.job_request = []
        job_obj.job_address = []
        for a in selector.xpath('//div[@class="work_addr"]/a'):
             job_obj.job_address.append(a.xpath('text()'))
        for c in selector.xpath('//dd[@class="job_bt"]/div/p'):
            job_obj.job_description.append(c.xpath('text()'))
        for k in selector.xpath('//dd[@class="job_request"]/p/span'):
            if 'class' not in k.keys():
                job_obj.job_request.append(k.xpath('text()'))

    def parse_jobs(self, response):
        self.parse_job_page(response)


