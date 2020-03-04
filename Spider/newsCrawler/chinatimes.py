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

class ChinatimesSpider(scrapy.Spider):
	name = 'chinatimes'
	allowed_domains = ['chinatimes.com']

	news_datetime_format = "%Y-%m-%d %H:%M:%S"


	def start_requests(self):
		self.MAX_PAGES = 1
		self._pages = 1
		# real time news
		yield scrapy.Request("https://www.chinatimes.com/realtimenews/?page=1&chdtv", callback=self.parse)

	def parse(self, response):
		for xpath_obj in response.xpath('//div[@class="articlebox-compact"]/div/div/h3/a'):
			url = response.urljoin(xpath_obj.xpath('./@href').extract_first())
			request = scrapy.Request(url, callback=self.parse_post)
			yield request

		self._pages += 1
		if self._pages <= self.MAX_PAGES:
			# get next page way
			next_page = response.xpath('//a[@class="page-link"]/@href').extract()[-2]
			if next_page:
				url = response.urljoin(next_page)
				logging.warning('follow {}'.format(url))
				yield scrapy.Request(url, callback=self.parse)
			else:
				logging.warning('no next page')
		else:
			logging.warning('max pages reached')

	def parse_post(self, response):
		news_title = response.xpath('//h1[@class="article-title"]/text()').extract_first()
		new_category = response.xpath('//meta[@name="section"]/@content').extract_first()
		news_author = response.xpath('//div[@class="author"]/a/text()').extract_first()
		news_datetime = response.xpath('//div[@class="meta-info"]/time/@datetime').extract_first()
		article_contant = response.xpath('//div[@class="article-body"]/p/text()').extract()
		images = response.xpath('//div[@class="photo-container"]/img/@scr').extract()
		keywords = response.xpath('//div[@class="article-hash-tag"]/span/a/text()').extract()

		item = SpiderItem()
		item['news_name'] = ChinatimesSpider.name
		item['url'] = response.url
		item['title'] = news_title
		item['news_no'] = re.sub(r'.*/(\d+)-.*' ,r'\1', response.url)
		item['category'] = new_category
		item['author'] = news_author
		item['datetime'] = datetime.strptime(news_datetime.strip(), '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(images)
		item['keywords'] = ','.join(keywords)
		yield item