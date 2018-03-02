#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 14:28
# @Author  : Dengsc
# @Site    : 
# @File    : ippools.py
# @Software: PyCharm


import os
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database_url = 'sqlite:///' + os.path.join(os.path.join(base_dir, 'proxy-saver'), 'proxy-data.sqlite')

engine = create_engine(database_url, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxy_ip'

    id = Column(String(128), primary_key=True)
    ip = Column(String(64))
    port = Column(Integer)
    type = Column(String(10))

    def __repr__(self):
        return '<Proxy {type}://{ip}:{port}>'.format(type=self.type, ip=self.ip, port=self.port)


def get_random_proxy():
    ip_obj = session.query(Proxy).order_by(func.random()).first()
    return '{type}://{ip}:{port}'.format(type=str(ip_obj.type).lower(), ip=ip_obj.ip, port=ip_obj.port)


if __name__ == '__main__':
    print get_random_proxy()
