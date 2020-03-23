# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                                    password="root", database="liming", charset="utf8")

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
            cursor = self.conn.cursor()
            cursor.execute(sql, tuple(dict_data.values()))

            # 提交
            # self.conn.commit()

        return item

    def get_by_detail(self, detail_url):
        sql = "select * from project_kor_krm where detail_url=%s"
        cursor = self.conn.cursor()
        cursor.execute(sql, (detail_url))
        return cursor.fetchall()

    def close_spider(self, spider):
        self.conn.close()
