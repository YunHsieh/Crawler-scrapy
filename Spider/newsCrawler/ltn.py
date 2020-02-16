"""
Crawl name : udn
create date : 2020/02/16
Author : Jerry Hsieh
"""


import scrapy
import logging
from scrapy.http import FormRequest
from spiderSettings.items import SpiderItem
from datetime import datetime
import re
import json

class LtnSpider(scrapy.Spider):
	name = 'ltn'
	allowed_domains = ['ltn.com.tw']

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	def start_requests(self):
		MAX_PAGES = 1

		formdata = {}

		for i in range(0,MAX_PAGES,1):
			yield scrapy.Request("https://news.ltn.com.tw/ajax/breakingnews/all/%s" % (str(i+1)))

	def parse(self, response):

		jsonresponse = json.loads(response.body_as_unicode())
		item = {}
		for _dict in jsonresponse['data']:
			url = response.urljoin(_dict['url'])
			item['title'] = _dict['title']
			item['news_no'] = _dict['no']
			item['category'] = _dict['tagText']
			yield scrapy.Request(url, callback=self.parse_post, meta={'item': item})

	def parse_post(self, response):
		news_datetime = response.xpath('//div[@class="text boxTitle boxText"]/span/text()').extract_first()
		article_contant = response.xpath('//div[@class="text boxTitle boxText"]/p/text()').extract()
		images = response.xpath('//div[@class="photo boxTitle"]/a/img/@scr').extract()
		keywords = response.xpath('//meta[@name="keywords"]/@content').extract_first()

		item = response.meta['item']
		item['news_name'] = LtnSpider.name
		item['url'] = response.url
		item['author'] = re.sub(r'[\u3014](.*)[\u3015].*',r'\1',article_contant[0])
		item['datetime'] = datetime.strptime(news_datetime.strip(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(images)
		item['keywords'] = keywords
		yield item