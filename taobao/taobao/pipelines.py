# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from orm import DB_Session


class MysqlPipeline(object):

    def save_to_mysql(self, data: dict, spider, db_table, query_filter, exist_is_update):
        if all([filed in data.keys() for filed in query_filter]):
            db_object = self.db_session.query(db_table) \
                .filter(*(getattr(db_table, query) == data[query] for query in query_filter)).first()
            if not isinstance(db_object, db_table):
                db_object = db_table(**data)
            else:
                if exist_is_update:
                    db_object.update(data)
            self.db_session.add(db_object)
            self.cache_num += 1
            if self.cache_num > self.max_cache_num:
                self.db_session.commit()
                self.cache_num = 0
        else:
            spider.logger.error('缺少必须的查询字段')

    def process_item(self, item, spider):
        if len(item) == 0:
            raise DropItem('空的item')
        db_table = spider.mysql_tables.get(item.__class__.__name__)
        query_filter = spider.query_filter.get(item.__class__.__name__)
        exist_is_update = spider.exist_is_update.get(item.__class__.__name__)
        if db_table and query_filter and exist_is_update is not None:
            keys = list(item.keys())
            if not isinstance(item[keys[0]], list):
                self.save_to_mysql(item, spider, db_table, query_filter, exist_is_update)
            else:
                values = [v for v in zip(*[item[k] for k in keys])]
                for single in values:
                    # 将有值的字段更新
                    data = {key: val for key, val in zip(keys, single) if val is not None}
                    if data:
                        self.save_to_mysql(data, spider, db_table, query_filter, exist_is_update)

        return item

    def open_spider(self, spider):
        self.db_session = DB_Session()
        self.max_cache_num = 10
        self.cache_num = 0

    def close_spider(self, spider):
        self.db_session.commit()
        self.db_session.close()
