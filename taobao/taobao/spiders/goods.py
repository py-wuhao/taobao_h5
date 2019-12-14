# -*- coding: utf-8 -*-
"""
经测试请求只需要data字段
提取商品 销量，分类，价格
不对请求过滤
"""
import json
import pickle
import re
import time

import redis
import scrapy
from faker import Faker
from scrapy_redis.spiders import RedisSpider

from orm import KuaishouGoods
from taobao.items import GoodsItem
from utial.goods_url import get_goods_url

_faker = Faker()


class GoodsSpider(RedisSpider):
    mysql_tables = {
        'GoodsItem': KuaishouGoods,
    }
    exist_is_update = {
        'GoodsItem': True,
    }
    query_filter = {
        'GoodsItem': ['pid'],
    }
    name = 'goods'
    redis_key = 'taobao_goods:urls'
    allowed_domains = ['taobao.com']
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        # 'LOG_FILE': 'logs/{name}-{time}.log'.format(name=name, time=time.strftime('%Y-%m-%d', time.localtime())),
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.2,
        'TAOBAO_THROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.2,
        'DOWNLOAD_REST': 30,
        'AUTOTHROTTLE_MAX_DELAY': 1,
        'STEP_DELAY': 0.05,

        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': None,
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'REDIS_URL': 'redis://auth:team1201@172.19.10.200:6379/1',

        'EXTENSIONS': {
            'extensions.taobao_throttle.TaoBaoThrottle': 500,
        },
        'ITEM_PIPELINES': {
            'taobao.pipelines.MysqlPipeline': 300,

        },
    }

    def make_request_from_data(self, data):
        pid, item_id = pickle.loads(data)
        url = get_goods_url(item_id)
        return scrapy.http.Request(url=url,
                                   callback=self.parse,
                                   dont_filter=True,
                                   meta={'pid': pid},
                                   headers={'user_agent': _faker.user_agent()}
                                   )

    def parse(self, response):
        if response.status != 200:
            pass
            return
        try:
            resp = json.loads(response.text)
            ret = resp.get('ret', [''])[0]
            if 'SUCCESS' in ret:
                goods = GoodsItem()
                value = json.loads(resp['data']['apiStack'][0]['value'])
                goods['pid'] = response.meta['pid']
                goods['sales_volume'] = self.srt_to_num(value['item'].get('vagueSellCount'))
                # goods['price'] = int(value['price']['price']['priceMoney'])
                # goods['market_price'] = int(
                #     value['price'].get('extraPrices', [{}])[0].get('priceMoney', goods['price']))
                goods['category_id'] = resp['data']['item']['rootCategoryId']
                yield goods
            elif 'FAIL_SYS_TRAFFIC_LIMIT' in ret:
                self.logger.warning('请求太快了')
                # 重新放回redis
                r = redis.Redis(host='172.19.10.200', port=6379, password='team1201', db=1)
                r.rpush(GoodsSpider.redis_key, pickle.dumps((response.meta['goods_id'], response.meta['item_id'])))
        except Exception as e:
            self.logger.error(e.args)

    @staticmethod
    def srt_to_num(s):
        if s:
            s = re.match(r'(\d+)(\w?)\+?', s)
            if s:
                n = float(s.group(1))
                if '万' == s.group(2):
                    n = n * 10000
                return int(n)
