# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 10:32
# @Author  : wuhao
# @Email   : 15392746632@qq.com
# @File    : taobao_throttle.py
# @Software: PyCharm
"""
淘宝请求速度控制
当响应出现‘哎哟喂,被挤爆啦,请稍后重试!’暂停DOWNLOAD_REST然后把下载延时STEP_DELAY
"""

import logging
import time

from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class TaoBaoThrottle(object):

    def __init__(self, crawler):
        self.crawler = crawler
        if not crawler.settings.getbool('TAOBAO_THROTTLE_ENABLED'):
            raise NotConfigured

        self.target_concurrency = crawler.settings.getfloat("AUTOTHROTTLE_TARGET_CONCURRENCY")
        crawler.signals.connect(self._spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self._response_downloaded, signal=signals.response_downloaded)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _spider_opened(self, spider):
        self.mindelay = self._min_delay(spider)
        self.maxdelay = self._max_delay(spider)
        self.rest = self._rest(spider)
        self.step_delay = self._step_delay(spider)
        spider.download_delay = self._start_delay(spider)

    def _min_delay(self, spider):
        s = self.crawler.settings
        return getattr(spider, 'download_delay', s.getfloat('DOWNLOAD_DELAY'))

    @staticmethod
    def _rest(spider):
        return spider.settings.getfloat('DOWNLOAD_REST')

    @staticmethod
    def _step_delay(spider):
        return spider.settings.getfloat('STEP_DELAY')

    def _max_delay(self, spider):
        return self.crawler.settings.getfloat('AUTOTHROTTLE_MAX_DELAY')

    def _start_delay(self, spider):
        return max(self.mindelay, self.crawler.settings.getfloat('AUTOTHROTTLE_START_DELAY'))

    def _response_downloaded(self, response, request, spider):
        if len(response.body) > 1000:
            # 正常响应
            return
        time.sleep(self.rest)
        logger.debug(f'请求过快休息{self.rest}')
        key, slot = self._get_slot(request, spider)
        latency = request.meta.get('download_latency')
        if latency is None or slot is None:
            return
        self._adjust_delay(slot, latency, response)

    def _get_slot(self, request, spider):
        key = request.meta.get('download_slot')
        return key, self.crawler.engine.downloader.slots.get(key)

    def _adjust_delay(self, slot, latency, response):
        """Define delay adjustment policy"""

        new_delay = slot.delay + self.step_delay
        new_delay = min(max(self.mindelay, new_delay), self.maxdelay)
        if response.status != 200 and new_delay <= slot.delay:
            return
        logger.debug(f'当前下载延时{new_delay}')
        slot.delay = new_delay
