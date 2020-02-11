"""
Crawl name : setn
update : 2020/02/07
Author : Jerry Hsieh
"""


import scrapy
import logging
from scrapy.http import FormRequest
from spiderSettings.items import SpiderItem
from datetime import datetime
import re

class SetnSpider(scrapy.Spider):
	name = 'setn'
	allowed_domains = ['setn.com']
	start_urls = ('https://www.setn.com/ViewAll.aspx?p=1', )

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	_retries = 0
	MAX_RETRY = 1

	_pages = 1
	MAX_PAGES = 1

	def parse(self, response):
		for xpath_obj in response.xpath('//h3[@class="view-li-title"]/a'):
			item = {}
			url = response.urljoin(xpath_obj.xpath('./@href').extract_first())
			item['shortened_title'] = xpath_obj.xpath('./text()').extract_first()
			request = scrapy.Request(url, callback=self.parse_post, meta={'item': item})
			yield request

		self._pages += 1
		if self._pages <= NBASpider.MAX_PAGES:
			# get next page way
			next_page = "/ViewAll.aspx?p=" + str(self._pages)
			if next_page:
				url = response.urljoin(next_page)
				logging.warning('follow {}'.format(url))
				yield scrapy.Request(url, self.parse)
			else:
				logging.warning('no next page')
		else:
			logging.warning('max pages reached')

	def parse_post(self, response, *args, **kwargs):
		title_info = response.xpath('//h1[@class="news-title-3"]//text()').extract_first()
		news_datetime = response.xpath('//div[@class="page-title-text"]/time//text()').extract_first()
		# basic_info = response.xpath('//div[@class="shareBar__info--author"]//text()').extract()
		author = response.xpath('//meta[@name="author"]/@content').extract_first()
		article_contant = response.xpath('//div[@class="page-text"]/div/article/div/p//text()').extract()
		images = response.xpath('//a[@data-target="#photo_view"]/img/@scr').extract()
		keywords = response.xpath('//div[@class="keyword page-keyword-area"]/ul/li/a/strong//text()').extract()
		category = response.xpath('//meta[@property="article:section"]/@content').extract_first()
		
		item = response.meta['item']
		item['news_no'] = re.sub(r'.*NewsID=(\d+)',r'\1',response.url)
		item['news_name'] = SetnSpider.name
		item['url'] = response.url
		item['title'] = title_info
		item['author'] = author
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(images)
		item['datetime'] = datetime.strptime(news_datetime, "%Y/%m/%d %H:%M:%S")
		item['category'] = category
		item['keywords'] = ','.join(keywords)
			# return event
		yield item