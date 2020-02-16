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

class GlobalnewstvSpider(scrapy.Spider):
	name = 'globalnewstv'
	allowed_domains = ['globalnewstv.com.tw']

	news_datetime_format = "%Y-%m-%d %H:%M:%S"

	def start_requests(self):
		MAX_PAGES = 1

		formdata = {
			'ajax-request':'jnews',
			'lang':'zh_TW',
			'action':'jnews_module_ajax_jnews_block_3',
			'module':'true',
			'data%5Bfilter%5D':'0',
			'data%5Bfilter_type%5D':'all',
			'data%5Bcurrent_page%5D':'1',
			'data%5Battribute%5D%5Bheader_icon%5D':'',
			'data%5Battribute%5D%5Bfirst_title%5D':'%E5%8D%B3%E6%99%82%E6%96%B0%E8%81%9E',
			'data%5Battribute%5D%5Bsecond_title%5D':'%3Cspan+style%3D%22padding-left%3A+10px%3B+color%3Ared%3B%22%3EJUST+IN%3C%2Fspan%3E',
			'data%5Battribute%5D%5Burl%5D':'',
			'data%5Battribute%5D%5Bheader_type%5D':'heading_3',
			'data%5Battribute%5D%5Bheader_background%5D':'',
			'data%5Battribute%5D%5Bheader_secondary_background%5D':'',
			'data%5Battribute%5D%5Bheader_text_color%5D':'',
			'data%5Battribute%5D%5Bheader_line_color%5D':'',
			'data%5Battribute%5D%5Bheader_accent_color%5D':'',
			'data%5Battribute%5D%5Bheader_filter_category%5D':'',
			'data%5Battribute%5D%5Bheader_filter_author%5D':'',
			'data%5Battribute%5D%5Bheader_filter_tag%5D':'',
			'data%5Battribute%5D%5Bheader_filter_text%5D':'All',
			'data%5Battribute%5D%5Bpost_type%5D':'post',
			'data%5Battribute%5D%5Bcontent_type%5D':'all',
			'data%5Battribute%5D%5Bnumber_post%5D':'5',
			'data%5Battribute%5D%5Bpost_offset%5D':'0',
			'data%5Battribute%5D%5Bunique_content%5D':'disable',
			'data%5Battribute%5D%5Binclude_post%5D':'',
			'data%5Battribute%5D%5Bexclude_post%5D':'',
			'data%5Battribute%5D%5Binclude_category%5D':'',
			'data%5Battribute%5D%5Bexclude_category%5D':'',
			'data%5Battribute%5D%5Binclude_author%5D':'',
			'data%5Battribute%5D%5Binclude_tag%5D':'',
			'data%5Battribute%5D%5Bexclude_tag%5D':'',
			'data%5Battribute%5D%5Bsort_by%5D':'latest',
			'data%5Battribute%5D%5Bdate_format%5D':'custom',
			'data%5Battribute%5D%5Bdate_format_custom%5D':'m%2Fd+H%3Ai',
			'data%5Battribute%5D%5Bexcerpt_length%5D':'0',
			'data%5Battribute%5D%5Bexcerpt_ellipsis%5D':'',
			'data%5Battribute%5D%5Bpagination_mode%5D':'loadmore',
			'data%5Battribute%5D%5Bpagination_number_post%5D':'5',
			'data%5Battribute%5D%5Bpagination_scroll_limit%5D':'0',
			'data%5Battribute%5D%5Bads_type%5D':'disable',
			'data%5Battribute%5D%5Bads_position%5D':'1',
			'data%5Battribute%5D%5Bads_random%5D':'',
			'data%5Battribute%5D%5Bads_image%5D':'',
			'data%5Battribute%5D%5Bads_image_link%5D':'',
			'data%5Battribute%5D%5Bads_image_alt%5D':'',
			'data%5Battribute%5D%5Bads_image_new_tab%5D':'',
			'data%5Battribute%5D%5Bgoogle_publisher_id%5D':'',
			'data%5Battribute%5D%5Bgoogle_slot_id%5D':'',
			'data%5Battribute%5D%5Bgoogle_desktop%5D':'auto',
			'data%5Battribute%5D%5Bgoogle_tab%5D':'auto',
			'data%5Battribute%5D%5Bgoogle_phone%5D':'auto',
			'data%5Battribute%5D%5Bcode%5D':'',
			'data%5Battribute%5D%5Bads_bottom_text%5D':'',
			'data%5Battribute%5D%5Bscheme%5D':'normal',
			'data%5Battribute%5D%5Bcolumn_width%5D':'auto',
			'data%5Battribute%5D%5Btitle_color%5D':'',
			'data%5Battribute%5D%5Baccent_color%5D':'',
			'data%5Battribute%5D%5Balt_color%5D':'',
			'data%5Battribute%5D%5Bexcerpt_color%5D':'',
			'data%5Battribute%5D%5Bcss%5D':'',
			'data%5Battribute%5D%5Bpaged%5D':'1',
			'data%5Battribute%5D%5Bcolumn_class%5D':'jeg_col_1o3',
			'data%5Battribute%5D%5Bclass%5D':'jnews_block_3',
		}

		for i in range(0,MAX_PAGES,1):
			formdata['data%5Bcurrent_page%5D'] = str(int(formdata['data%5Bcurrent_page%5D']) + 1)
			prams_data = '&'.join(["%s=%s" % (i,k) for i, k in formdata.items()])
			yield scrapy.Request("http://globalnewstv.com.tw/?"+prams_data)

	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		selector = scrapy.Selector(text=jsonresponse['content'], type="html")
		for href in selector.xpath("//div/h3/a/@href").extract():
			url = response.urljoin(href)

			yield scrapy.Request(url, callback=self.parse_post)

	def parse_post(self, response):
		title_info = response.xpath('//h1[@class="jeg_post_title"]/text()').extract()
		news_datetime = response.xpath('//div[@class="jeg_meta_date"]/a/text()').extract_first()
		# this new no author
		# author = response.xpath('//span[@class="article-content__author"]/a/text()').extract_first()
		article_contant = response.xpath('//div[@class="content-inner "]/p/text()').extract()
		images = response.xpath('//div[@class="jeg_featured featured_image"]/a/@href').extract()
		keywords = response.xpath('//div[@class="jeg_post_tags"]/a/text()').extract()
		# category = response.xpath('//nav[@class="article-content__breadcrumb"]/a/text()').extract()[1]

		item = SpiderItem()
		item['title'] = ' '.join(title_info)
		item['news_no'] = re.sub(r'(\d+).*',r'\1',response.url.split('/')[-2])
		item['news_name'] = GlobalnewstvSpider.name
		item['url'] = response.url
		item['author'] = ''
		item['datetime'] = datetime.strptime(str(datetime.now().year)+news_datetime,'%Y%m/%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
		item['content'] = '\n'.join(article_contant)
		item['images'] = ','.join(images)
		item['category'] = ''
		item['keywords'] = ','.join(keywords)
			# return event
		yield item