#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 13:23
# @Author  : Dengsc
# @Site    : 
# @File    : quickstart.py
# @Software: PyCharm


from scrapy import cmdline


cmdline.execute('scrapy crawl lagou'.split())
