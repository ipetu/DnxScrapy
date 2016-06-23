#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/5/8
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

from items import QsbkItem


class DmozSpider(CrawlSpider):
    name = "qsbkcrawl"
    allowed_domains = ['www.qiushibaike.com']
    start_urls = [
        'http://www.qiushibaike.com/8hr/page/2/?s=4888977',
    ]
    rules = [
        Rule(LinkExtractor(allow=('^http://www.qiushibaike.com\/8hr\/page\/\d\/\?s=4888977')), callback='parse_list', follow=True),
        # Rule(LinkExtractor(allow=('/*')), callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        from scrapy import Selector
        sel = Selector(response)
        sites = sel.xpath('//*[@id="content-left"]/div[@class="article block untagged mb15"]')
        items = []
        for site in sites:
            item = QsbkItem()
            name= site.xpath('div[@class="content"]/text()').extract_first()
            nick = site.xpath('div[@class="author clearfix"]/a[2]/h2/text()').extract_first()
            avatarUrl = site.xpath('div[@class="author clearfix"]/a[1]/img/@src').extract_first()
            from scrapy.utils.request import request_fingerprint
            request = ''
            key = ''
            if avatarUrl is not None:
                request = Request(avatarUrl)
                key = '%s%s' % ('dq_', request_fingerprint(request))
            qiniuUrl = "http://o8y576gfk.bkt.clouddn.com/" + key+'.jpg'
            item['desc'] = name
            item['nick'] = nick
            item['avatarUrl'] = avatarUrl
            item['qiniuUrl'] = qiniuUrl
            items.append(item)
        return items
