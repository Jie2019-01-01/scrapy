# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KrmItem(scrapy.Item):
    dict_data = scrapy.Field()
    dict_data['title'] = {}
    dict_data['project_name'] = {}
    dict_data['program'] = {}
    dict_data['detail_url'] = {}
    dict_data['project_number'] = {}
    dict_data['year_selected'] = {}
    dict_data['research_period'] = {}
    dict_data['chief_of_research'] = {}
    dict_data['cooperation_researcher'] = {}
    dict_data['executing_organization'] = {}
    dict_data['research_executing_organization'] = {}
    dict_data['the_present_condition_of_project'] = {}
    dict_data['page'] = {}
    dict_data['abstract'] = {}