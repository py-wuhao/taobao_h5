# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 9:54
# @Author  : wuhao
# @Email   : 15392746632@qq.com
# @File    : from_mysql_to_redis.py
# @Software: PyCharm
import re
import pickle

import redis

from orm import KuaishouGoods, DB_Session
from taobao.spiders.goods import GoodsSpider


def get_goods(try_num=3) -> list:
    goods = []
    pattern = re.compile(r'id=(\d+$)')
    db_session = DB_Session()
    try:
        goods = db_session.query(KuaishouGoods) \
            .filter(KuaishouGoods.source == 2) \
            .order_by(KuaishouGoods.create_time.desc()) \
            .limit(5 * 10000).all()
    except:
        if try_num > 0:
            get_goods(try_num - 1)
    finally:
        db_session.close()
        result = []
        item_ids = set()
        for g in goods:
            item_id = pattern.findall(g.goods_link)
            item_ids.add(item_id[0])
            if item_id:
                result.append(pickle.dumps((g.pid, item_id[0])))
        print(item_ids)
        return result


def to_redis():
    r = redis.Redis(host='172.19.10.200', port=6379,password='team1201', db=1)
    all_goods = get_goods()
    for goods in all_goods:
        r.lpush(GoodsSpider.redis_key, goods)


if __name__ == '__main__':
    to_redis()
