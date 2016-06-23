#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/23
import scrapy
from datetime import datetime

from items import NewQsbkItem


class QiuShiBaiKe(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = [
        "http://www.qiushibaike.com",
    ]

    def parse(self, response):
        for article in response.xpath("//div[contains(@class, 'article')]"):
            item = NewQsbkItem()
            author_sel = article.xpath('div[contains(@class, "author")]/a')
            item['header'] = author_sel.xpath('img/@src').extract()  # 用户头像
            item['author'] = "".join(author_sel.xpath('h2/text()').extract()).strip()  # 用户名称
            content_sel = article.xpath('div[@class="content"]')
            item['content'] = content_sel.xpath('text()').extract()  # 内容
            item['created_at'] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")  # content_sel.xpath('@title').extract()     # 内容创建日期
            item['thumb'] = article.xpath("div[contains(@class, 'thumb')]/a/img/@src").extract()  # 内容附件图片

            yield item
        # 得到下一页链接地址
        next_href = response.xpath(
            "//ul[contains(@class, 'pagination')]/li/a/span[contains(@class, 'next')]/../@href").extract_first()
        url = "http://www.qiushibaike.com" + next_href.strip()
        current_pageNo = response.xpath(
            '//ul[contains(@class, "pagination")]/li/span[contains(@class, "current")]/text()').extract()
        current = current_pageNo[0].strip()
        # 只爬取首页面的35页内容
        if (int(current) != 35):
            yield scrapy.Request(url,  callback=self.parse)
