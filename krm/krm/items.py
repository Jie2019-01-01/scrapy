# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KrmItem(scrapy.Item):
    dict_data = scrapy.Field()
    dict_data['title'] = {}
    dict_data['program'] = {}
    dict_data['detail_url'] = {}
    dict_data['project_number'] = {}
    dict_data['year'] = {}
    dict_data['period'] = {}
    dict_data['leader'] = {}
    dict_data['organization'] = {}
    dict_data['project_condition'] = {}
    dict_data['page'] = {}
