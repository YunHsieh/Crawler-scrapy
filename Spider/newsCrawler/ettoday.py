"""
Crawl name : NBA
create date : 2019/07/16
Author : Jerry Hsieh
"""


import scrapy
import logging
from scrapy.http import FormRequest
from spiderSettings.items import SpiderItem
from datetime import datetime
import re
import json

class EttodaySpider(scrapy.Spider):
	name = 'ettoday'
	allowed_domains = ['ettoday.net']

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	def start_requests(self):
		MAX_PAGES = 10

		formdata = {
			"offset" : '1',
			"tPage" : '3',
			"tFile" : datetime.now().strftime('%Y%m%d')+".xml"
		}

		for i in range(0,MAX_PAGES,1):
			formdata['offset'] = str(int(formdata['offset']) + 1)
			yield FormRequest("https://www.ettoday.net/show_roll.php",
					formdata=formdata,
					callback=self.parse)

	def parse(self, response):
		for href in response.xpath('//h3/a/@href').extract():
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_post)

	def parse_post(self, response):
		basic_info = response.xpath('//script[@type="application/ld+json"]/text()').extract_first().strip()
		basic_info = json.loads(basic_info)
		article_contant = response.xpath('//article/div/div/p/text()').extract()
		if not article_contant:
			article_contant = response.xpath('//article/div/p/text()').extract()


		
		item = SpiderItem()
		item['news_no'] = re.sub(r'(\d+).*',r'\1',response.url.split('/')[-1])
		item['news_name'] = EttodaySpider.name
		item['url'] = response.url
		item['title'] = basic_info['headline']
		item['author'] = basic_info['creator'][0]
		item['content'] = '\n'.join(article_contant)
		item['images'] = basic_info['url']
		item['datetime'] = datetime.strptime(basic_info['datePublished'][:-6], '%Y-%m-%dT%H:%M:%S')
		item['category'] = basic_info['articleSection']
		item['keywords'] = ','.join(basic_info['keywords'])
			# return event
		yield item