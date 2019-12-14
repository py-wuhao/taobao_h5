# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import BIGINT

from .base import BaseModelPro


class GoodsInfo(BaseModelPro):
    __abstract__ = True
    # id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    # pid = Column(String(255))
    # title = Column(String(32))
    # image_link = Column(String(255))
    # goods_link = Column(String(1024))
    # sales_volume = Column(Integer)
    # price = Column(Integer)
    # market_price = Column(Integer)
    # source = Column(Integer)
    # visitor_num = Column(Integer)
    # # category_id = Column(Integer, comment='分类id')
    # goods_update_time = Column(TIMESTAMP)
    id = Column(BIGINT(unsigned=True), autoincrement=True, primary_key=True)
    goods_id = Column(BIGINT(unsigned=True), nullable=False)
    title = Column(String(32))
    image_link = Column(String(255))
    goods_link = Column(String(4096))
    sales_volume = Column(Integer)
    price = Column(Integer)
    market_price = Column(Integer)
    source = Column(Integer)
    visitor_num = Column(Integer)
    pid = Column(String(255))


class KuaishouGoods(GoodsInfo):
    __tablename__ = 'kuaishou_goods'


class DouyinGoods(GoodsInfo):
    __tablename__ = 'douyin_goods'
