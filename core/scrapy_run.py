import sys
sys.path.append('spider')
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings

from spider.spiderSettings import settings as my_settings
from spider.newsCrawler.nba import NBASpider

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)

def run_scrapy(ob_scr):
	c = CrawlerRunner(
		crawler_settings
	)
	c.crawl(ob_scr)
	d = c.join()
	d.addBoth(lambda _: reactor.stop())
	# reactor.callFromThread(notThreadSafe, 3)
	reactor.run()
	# c.start()

# run_scrapy(NBASpider)