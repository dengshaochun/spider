#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 15:02
# @Author  : Dengsc
# @Site    : 
# @File    : models.py
# @Software: PyCharm


import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL


logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, echo=True)
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


def create_tables():
    logger.info('create tables')
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_tables()
