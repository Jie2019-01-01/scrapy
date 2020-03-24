# -*- coding: utf-8 -*-
import scrapy
from ..items import KrmItem
import re
from copy import deepcopy


class KrmSpiderSpider(scrapy.Spider):
    name = 'krm_spider'
    allowed_domains = ['www.krm.or.kr']
    start_urls = ['https://www.krm.or.kr/krmts/bird/advanceSearch.html?actionUrl=%2Fkrmts%2Fbird%2FadvanceSearch.html&searchWord=&executeQuery=%28date%3A%255B*%2520TO%252020201231%255D%29%2520and%2520z_data_cd%3AResearch%2520-ISNEW%3AY&frbrDataTypeCd=research&searchType=research&flag=&z_class=n&requery=%28date%3A%255B*%2520TO%252020201231%255D%29%2520and%2520z_data_cd%3AResearch%2520-ISNEW%3AY&viewQueryString=%EC%84%A0%EC%A0%95%EC%97%B0%EB%8F%84%2F1985%EC%9D%B4%EC%A0%84%2C%EC%84%A0%EC%A0%95%EC%97%B0%EB%8F%84%2F20201231%2C&listPerPage=20&classificationId=KRF']

    def parse(self, response):

        td1 = response.xpath('//a[@class="kfont06"]')
        if len(td1) == 0:
            return

        td2 = response.xpath('//a[@class="kfont06"]/ancestor::tr[1]/following-sibling::tr[1]/td')
        for i in range(len(td1)):
            item = KrmItem()
            # 声明item['dict_data']的类型为字典
            dict_data = item['dict_data'] = {}

            profession = td2[i].xpath('string(.)').extract_first()
            if profession.find('Program : ') != -1:
                program = profession.split('Program : ')[-1]
            else:
                program = ''
            dict_data['project_name'] = ''.join(program.split())

            href = td1[i].xpath('./@href').extract_first()
            vals = re.findall("'.*?'", href)
            detail_url = 'https://www.krm.or.kr/krmts/search/detailview/research.html?metaDataId='+ vals[2] +\
                         '&local_id=' + vals[3] + '&dbGubun=' + vals[0] +\
                         '&m201_id='+ vals[4] +'&m301_arti_id=' +\
                         '&category='+ vals[1]
            detail_url = detail_url.replace("'", '')

            # callback为请求detail_url之后的回调，meta用来传递item，值是字典
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': deepcopy(item)})

        # 开始下一页
        next_href = response.xpath('//span[@class="p_select"]/following-sibling::span[1]/a/@href').extract_first()
        page = next_href.split("'")[1]
        next_url = self.start_urls[0] + '&curPageNum=' + page
        yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 获取item
        item = response.meta.get('item')
        dict_data = item['dict_data']
        dict_temp = {}

        # 使用xpath在详情页取值
        td1 = response.xpath('//td[@class="kfont06"]')
        td2 = response.xpath('//td[@class="kfont15"]')
        for i in range(len(td1)):
            name = td1[i].xpath('./text()').extract_first()
            value = td2[i].xpath('string(.)').extract_first()
            dict_temp[name] = ' '.join(value.split())

        span = response.xpath('//div/span[@class="kfont09"]/text()').extract_first();
        title = ''.join(span.split())
        hw = re.findall(r"[\uac00-\ud7ffa-zA-Z0-9]+", title)
        title = ''.join(hw)

        dict_data['title'] = title
        dict_data['program'] = dict_temp.get('Program')
        dict_data['detail_url'] = response.request.url
        dict_data['project_number'] = dict_temp.get('Project Number')
        dict_data['year_selected'] = dict_temp.get('Year(selected)')
        dict_data['research_period'] = dict_temp.get('Research period')
        dict_data['chief_of_research'] = dict_temp.get('chief of research')
        dict_data['cooperation_researcher'] = dict_temp.get('Cooperation researcher')
        dict_data['executing_organization'] = dict_temp.get('Executing Organization')
        dict_data['research_executing_organization'] = dict_temp.get('Research Executing Organization')
        dict_data['the_present_condition_of_project'] = dict_temp.get('the present condition of Project')

        ab = response.xpath('string(//div[@class="researchSummary"])').extract_first()
        ab = re.sub('\s+', ' ', ab)
        hw = re.findall(r"[\uac00-\ud7ffa-zA-Z0-9]+", ab)
        dict_data['abstract'] = ' '.join(hw)

        yield item