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
from ..items import JobsItem


class DmozSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = [
        'https://www.lagou.com/'
    ]

    rules = [
        Rule(sle(allow=('/jobs/[0-9]+.html$')), callback='parse_jobs', follow=True),
        Rule(sle(allow=('/zhaoping/[a-zA-Z]+/$')), follow=True),
    ]

    def format_data(self, data):
        if isinstance(data, list):
            new_list = []
            for x in data:
                tmp = x.replace('\n', '').strip()
                if tmp != '':
                    new_list.append(tmp)
            return new_list
        elif isinstance(data, str):
            return data.replace('\n', '').strip()
        else:
            return data

    def parse_jobs(self, response):
        job_obj = JobsItem()
        selector = Selector(response)
        job_obj.link_url = self.format_data(response.url)
        job_obj.job_title = self.format_data(selector.xpath('//div[@class="job-name"]/div[@class="company"]/text()'))
        job_obj.job_name = self.format_data(selector.xpath('//div[@class="job-name"]/span[@class="name"]/text()'))
        job_obj.job_salary = self.format_data(selector.xpath('//span[@class="salary"]/text()'))
        job_obj.job_advantage = self.format_data(selector.xpath('//dd[@class="job-advantage"]/p/text()'))
        job_obj.job_positionLng = self.format_data(
            selector.xpath('//dd[@class="job-address clearfix"]/input[@name="positionLng"]/@value'))
        job_obj.job_positionLat = self.format_data(
            selector.xpath('//dd[@class="job-address clearfix"]/input[@name="positionLat"]/@value'))
        job_obj.job_positionAddress = self.format_data(
            selector.xpath('//dd[@class="job-address clearfix"]/input[@name="positionAddress"]/@value'))
        job_obj.job_workAddress = self.format_data(
            selector.xpath('//dd[@class="job-address clearfix"]/input[@name="workAddress"]/@value'))
        job_obj.company_name = self.format_data(selector.xpath('//dl[@class="job_company"]/dt/a/img/@alt'))
        job_obj.company_domain = self.format_data(selector.xpath('//ul[@class="c_feature"]/li')[0].xpath('text()'))
        job_obj.company_stage = self.format_data(selector.xpath('//ul[@class="c_feature"]/li')[1].xpath('text()'))
        job_obj.company_scale = self.format_data(selector.xpath('//ul[@class="c_feature"]/li')[2].xpath('text()'))
        job_obj.company_home_page = self.format_data(selector.xpath('//ul[@class="c_feature"]/li')[3].xpath('a/text()'))
        job_obj.job_description = []
        job_obj.job_request = []
        for c in selector.xpath('//dd[@class="job_bt"]/div/p'):
            if c.xpath('span'):
                for d in c.xpath('span'):
                    job_obj.job_description.append(self.format_data(d.xpath('text()')))
            else:
                job_obj.job_description.append(self.format_data(c.xpath('text()')))
        for k in selector.xpath('//dd[@class="job_request"]/p/span'):
            if 'class' not in k.keys():
                job_obj.job_request.append(self.format_data(k.xpath('text()')))
        yield job_obj


