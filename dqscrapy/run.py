#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/20
# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy import log, signals
# from scrapy.utils.project import get_project_settings
# from spiders.dqSpider import DmozSpider
#
# spider = DmozSpider()  #这里改为你的爬虫类名
# settings = get_project_settings()
# crawler = Crawler(settings)
# crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
# crawler.configure()
# crawler.crawl(spider)
# crawler.start()
# log.start()
# reactor.run()
from scrapy.cmdline import execute

execute()