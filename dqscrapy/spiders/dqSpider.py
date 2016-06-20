#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/5/8
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

from items import QsbkItem


class DmozSpider(CrawlSpider):
    name = "qsbkcrawl"
    start_urls = [
        "http://www.qiushibaike.com"
    ]
    rules = [
        Rule(LinkExtractor(allow=('/8hr/page/[1-3]*')), callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        from scrapy import Selector
        sel = Selector(response)
        sites = sel.xpath('//*[@id="content-left"]/div[@class="article block untagged mb15"]')
        items = []
        for site in sites:
            item = QsbkItem()
            nameList = site.xpath('div[@class="content"]/text()').extract()
            nickList = site.xpath('div[@class="author clearfix"]/a[2]/h2/text()').extract()
            avatarUrlList = site.xpath('div[@class="author clearfix"]/a[1]/img/@src').extract()
            name = ''
            nick = ''
            avatarUrl = ''
            qiniuUrl = ''
            if nameList is not None and len(nameList) > 0:
                name = nameList[0]
            if nickList is not None and len(nickList) > 0:
                nick = nickList[0]
            if avatarUrlList is not None and len(avatarUrlList) > 0:
                from scrapy.utils.request import request_fingerprint
                avatarUrl = avatarUrlList[0]
                request = Request(avatarUrl)
                key = '%s%s' % ('dq_', request_fingerprint(request))
                qiniuUrl = "http://o8y576gfk.bkt.clouddn.com/" + key+'.jpg'

            item['desc'] = name
            item['nick'] = nick
            item['avatarUrl'] = avatarUrl
            item['qiniuUrl'] = qiniuUrl
            items.append(item)
        return items
