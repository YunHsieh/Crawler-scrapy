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
	# start_urls = ('https://www.ettoday.net/show_roll.php', )
	fromdata = {
		"offset" : 1,
		"tPage" : 3,
		"tFile" : datetime.now().strftime('%Y%m%d')+".xml"
	}

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	_retries = 0
	MAX_RETRY = 1

	MAX_PAGES = 1

	def start_requests(self):
		for i in range(1,MAX_PAGES,1):
			fromdata[offset] += 1
			yield scrapy.Request("https://www.ettoday.net/show_roll.php",
					method='POST',
					formdata=fromdata,
					callback=self.parse)


	def parse(self, response):
		for href in response.xpath('//h3/a/@href').extract():
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_post)

	def parse_post(self, response):
		basic_info = response.xpath('//script[@type="application/ld+json"]/text()').extract_first().strip()
		basic_info = json.loads(basic_info)
		# title_info = response.xpath('//h1[@class="title"]//text()').extract_first()
		# news_datetime = response.xpath('//div[@class="page-title-text"]/time//text()').extract_first()
		# author = response.xpath('//script[@type="application/ld+json"]').extract_first()
		article_contant = response.xpath('//article/div[@class="subject_article"]/p/text()').extract()
		# images = response.xpath('//a[@data-target="#photo_view"]/img/@scr').extract()
		# keywords = response.xpath('//div[@class="keyword page-keyword-area"]/ul/li/a/strong//text()').extract()
		# category = response.xpath('//meta[@property="article:section"]/@content').extract_first()
		
		item = SpiderItem()
		item['id'] = re.sub(r'(\d+).*',r'\1',response.url.split('/')[-1])
		item['news_name'] = name
		item['url'] = response.url
		item['title'] = basic_info['headline']
		item['author'] = basic_info['creator'][0]
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(basic_info['url'])
		item['datetime'] = datetime.strptime(basic_info['datePublished'][:-6], '%Y-%m-%dT%H:%M:%S')
		item['category'] = basic_info['articleSection']
		item['keywords'] = basic_info['keywords']
			# return event
		yield item