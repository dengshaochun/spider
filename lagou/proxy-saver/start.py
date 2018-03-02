#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 14:51
# @Author  : Dengsc
# @Site    : 
# @File    : start.py
# @Software: PyCharm


import uuid
import requests
import logging
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Proxy
from lagou.user_agent import agents
import random
from lxml import etree
import threadpool

logger = logging.getLogger(__name__)

base_url = 'http://www.xicidaili.com/'
pats = ['nn/', 'nt/', 'wn/', 'wt/']
check_url = 'http://ip.chinaz.com/getip.aspx'


class ProxySaver(object):

    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_ips(self):
        for pat in pats:
            objs = []
            headers = {'content-type': 'application/json',
                       'User-Agent': random.choice(agents)}
            for i in range(100):
                ip_obj = self.session.query(Proxy).order_by(func.random()).first()
                proxies = {'{type}'.format(type=ip_obj.type):
                               '{type}://{ip}:{port}'.format(type=ip_obj.type, ip=ip_obj.ip, port=ip_obj.port)}
                url = '{base_url}{pat}{page}'.format(base_url=base_url, pat=pat, page=i)
                logger.info('Scrapy {url}'.format(url=url))
                try:
                    response = requests.get(url, headers=headers, proxies=proxies)
                    if response.status_code == 200:
                        selector = etree.HTML(response.text)
                        for line in selector.xpath('//table[@id="ip_list"]//tr[@class="odd"]'):
                            proxy_obj = Proxy()
                            proxy_obj.id = str(uuid.uuid1())
                            proxy_obj.ip = line.xpath('td')[1].xpath('text()')[0]
                            proxy_obj.port = line.xpath('td')[2].xpath('text()')[0]
                            proxy_obj.type = str(line.xpath('td')[5].xpath('text()')[0]).lower().replace('https', 'http')
                            objs.append(proxy_obj)
                except:
                    pass
            self._threads_check(objs)

    def _check_status(self, item):
        proxies = {'{type}'.format(type=str(item.type)): '{type}://{ip}:{port}'.format(type=str(item.type),
                                                                                       ip=item.ip,
                                                                                       port=item.port), }
        headers = {'content-type': 'application/json',
                   'User-Agent': random.choice(agents)}
        try:
            response = requests.get(check_url, headers=headers, proxies=proxies, timeout=2)
            logger.info('Check {type}://{ip}:{port} -> {status}'.format(
                type=item.type,
                ip=item.ip,
                port=item.port,
                status=item.ip in response.text))
            return True if item.ip in response.text else False
        except Exception as e:
            logger.error('Check {type}://{ip}:{port} -> error'.format(
                type=item.type,
                ip=item.ip,
                port=item.port))
            return False

    def _threads_check(self, objs):
        pool = threadpool.ThreadPool(20)
        request = threadpool.makeRequests(self._check_status, objs)
        [pool.putRequest(req) for req in request]
        pool.wait()

    def _save_to_db(self, item):
        try:
            flag = self.session.query(Proxy).filter(and_(
                Proxy.ip == item.ip,
                Proxy.port == item.port
            )).first()
            if not flag:
                self.session.add(item)
                self.session.commit()
                logger.info('Save obj: {obj}'.format(obj=str(item)))
            else:
                logger.warn('Exists obj: {obj}'.format(obj=str(item)))
        except Exception as e:
            logger.error(str(e))


if __name__ == '__main__':
    proxy_saver = ProxySaver()
    proxy_saver.get_ips()
