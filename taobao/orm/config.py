# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 15:03
# @Author  : wuhao
# @Email   : 15392746632@qq.com
# @File    : config.py
# @Software: PyCharm

# *******MySQL 配置***********

DB_CONNECT_STRING = 'mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}?charset={charset}'
LOCAL_DB_CONNECT_PARAMS = dict(
    user='root',
    password='general',
    hostname='127.0.0.1',
    port=3306,
    database='short_video',
    charset='utf8mb4'
)
PRODUCTION_DB_CONNECT_PARAMS = dict(
    user='root',
    password='Pwd_2019',
    hostname='172.19.10.200',
    port=3306,
    database='short_video',
    charset='utf8mb4'
)
config = {
    'local': LOCAL_DB_CONNECT_PARAMS,
    'production': PRODUCTION_DB_CONNECT_PARAMS,
}
DB_CONNECT_PARAMS = config['production']
