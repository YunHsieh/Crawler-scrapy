# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
	def process_item(self, item, spider):
		item.setdefault('shortened_title', '')
		item.setdefault('author', '')
		item.setdefault('images', '')
		item.setdefault('category', '')
		item.setdefault('keywords', '')
		return item
