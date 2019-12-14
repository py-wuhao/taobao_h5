# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 9:39
# @Author  : wuhao
# @Email   : 15392746632@qq.com
# @File    : goods_url.py
# @Software: PyCharm
import hashlib
import json
import urllib.parse
import time


def sign(t: str, data: str):
    token = 'undefined'
    a = '12574478'
    s = token + '&' + t + '&' + a + '&' + data
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()


def get_goods_url(item_id):
    t = str(int(time.time() * 1000))
    goods_url = r'http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?'
    data = {
        'id': str(item_id),
        'itemNumId': str(item_id),
        'itemId': str(item_id),
        'exParams': '{{"id":"{}"}}'.format(item_id),
        'detail_v': '8.0.0',
        'utdid': '1'
    }
    data_str = json.dumps(data, separators=(',', ':'))
    query = {'jsv': '2.5.1',
             'appKey': '12574478',
             't': t,
             'sign': sign(t, data_str),
             'api': 'mtop.taobao.detail.getdetail',
             'v': '6.0',
             'isSec': '0',
             'ecode': '0',
             'AntiFlood': 'true',
             'AntiCreep': 'true',
             'H5Request': 'true',
             'ttid': '2018@taobao_h5_9.9.9',
             'type': 'jsonp',
             'dataType': 'jsonp',
             'data': data_str
             }

    query = urllib.parse.urlencode(query)
    return goods_url + query
