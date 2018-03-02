# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import log
from pymongo import IndexModel, ASCENDING
from items import JobsItem


class LagouPipeline(object):

    def __init__(self):
        clinet = pymongo.MongoClient('localhost', 27017)
        db = clinet['lagou']
        self.PhRes = db['PhRes']
        idx = IndexModel([('link_url', ASCENDING)], unique=True)
        self.PhRes.create_indexes([idx])

    def process_item(self, item, spider):
        """ 判断类型 存入MongoDB """
        if isinstance(item, JobsItem):
            try:
                log.INFO('MongoDBItem: {url}'.format(url=item.link_url))
                self.PhRes.update_one({'link_url': item.link_url}, {'$set': dict(item)}, upsert=True)
            except Exception:
                pass
        return item
