# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 16:03
# @Author  : wuhao
# @Email   : 15392746632@qq.com
# @File    : base.py
# @Software: PyCharm

from sqlalchemy import create_engine, Column, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_CONNECT_STRING, DB_CONNECT_PARAMS

engine = create_engine(DB_CONNECT_STRING.format(**DB_CONNECT_PARAMS))
DB_Session = sessionmaker(bind=engine)
BaseModel = declarative_base()


class BaseModelPro(BaseModel):
    __abstract__ = True
    create_time = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    update_time = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    def update(self, data: dict):
        for key, val in data.items():
            setattr(self, key, val)
