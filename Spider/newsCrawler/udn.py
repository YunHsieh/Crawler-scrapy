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

class UdnSpider(scrapy.Spider):
	name = 'udn'
	allowed_domains = ['udn.com.tw']

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	def start_requests(self):
		MAX_PAGES = 1

		formdata = {}

		for i in range(0,MAX_PAGES,1):
			yield scrapy.Request("http://udn.com.tw/category/%e5%8f%b0%e7%81%a3%e4%bb%8a%e6%97%a5%e4%ba%8b/page/%s/" % (str(i)))

	def parse(self, response):
		url = response.xpath('//div[@class="jeg_posts jeg_load_more_flag"]/article/div/a/@href').extract()
		item = {}
		for _url in url:
			url = response.urljoin(_dict['titleLink'])
			item['title'] = _dict['title']
			item['datetime'] = datetime.strptime(_dict['time']['date'], '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
			yield scrapy.Request(url, callback=self.parse_post, meta={'item': item})

	def parse_post(self, response):
		title_info = response.xpath('//h1[@class="article-content__title"]//text()').extract_first()
		news_datetime = response.xpath('//time[@class="article-content__time"]//text()').extract_first()
		author = response.xpath('//span[@class="article-content__author"]/a/text()').extract_first()
		article_contant = response.xpath('//section[@class="article-content__editor "]/p/text()').extract()
		images = response.xpath('//picture/img/@scr').extract()
		keywords = response.xpath('//section[@class="keywords"]/a/text()').extract()
		category = response.xpath('//nav[@class="article-content__breadcrumb"]/a/text()').extract()[1]

		
		item = response.meta['item']
		item['news_no'] = re.sub(r'(\d+).*',r'\1',response.url.split('/')[-1])
		item['news_name'] = UdnSpider.name
		item['url'] = response.url
		item['author'] = author
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(images)
		item['category'] = category
		item['keywords'] = ','.join(keywords)
			# return event
		yield item