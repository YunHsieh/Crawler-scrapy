# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy_djangoitem import DjangoItem
# from core.models import row_news

# call model meta 
# default empty set in pipelines.py file.
class SpiderItem(scrapy.Item):
	id = scrapy.Field()
	url = scrapy.Field()
	title = scrapy.Field()
	news_name = scrapy.Field()
	shortened_title = scrapy.Field() # default empty
	author = scrapy.Field() # default empty
	content = scrapy.Field()
	images = scrapy.Field() # default empty
	datetime = scrapy.Field()
	category = scrapy.Field() # default empty
	keywords = scrapy.Field() # default empty
