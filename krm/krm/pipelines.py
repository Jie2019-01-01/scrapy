# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):

    def __init__(self, host, database, port, username, password):
        self.host = host
        self.database = database
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            database = crawler.settings.get('MYSQL_DATABASE'),
            port = crawler.settings.get('MYSQL_PORT'),
            username = crawler.settings.get('MYSQL_USERNAME'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username,
                            password=self.password, database=self.database, charset="utf8")
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        dict_data = item['dict_data']
        print(dict_data['detail_url'])

        count = self.get_by_detail(dict_data['detail_url'])
        if len(count) <= 0:
            # 创建sql语句
            key = ','.join(dict_data.keys())
            val = ','.join(['%s'] * len(dict_data))
            sql = 'insert into project_kor_krm(%s) values(%s)' % (key, val)

            # 创建游标
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, tuple(dict_data.values()))

            # 提交
            self.conn.commit()

        return item

    def get_by_detail(self, detail_url):
        sql = "select * from project_kor_krm where detail_url=%s"
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql, (detail_url))
        return self.cursor.fetchall()

    def close_spider(self, spider):
        self.conn.close()
