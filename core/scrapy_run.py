import sys
sys.path.append('spider')
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spider.spiderSettings import settings as my_settings
from spider.newsCrawler.nba import NBASpider

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)

def run_scrapy(ob_scr):
	c = CrawlerProcess(
		settings=crawler_settings
	)
	c.crawl(ob_scr)
	c.start()

# run_scrapy(NBASpider)