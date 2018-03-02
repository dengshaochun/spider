#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 15:04
# @Author  : Dengsc
# @Site    : 
# @File    : config.py
# @Software: PyCharm

import os
import logging

# 设置变量
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'proxy-data.sqlite')

# 初始化logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s')

