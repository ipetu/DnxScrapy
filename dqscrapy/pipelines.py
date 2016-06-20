# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from dqscrapy.impl import QiniuFilesStore


class DqscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class DqScrapyPipeline(object):
    def open_spider(self, spider):
        # self.dbconn = connect('douqu', host='192.168.1.45:27017')
        # self.connction = pymongo.Connection("192.168.1.45", 27017)
        # self.douqu = self.connction.douqu
        self.mongoClient = MongoClient("192.168.1.104", 27017)
        self.db = self.mongoClient.douqu

    def close_spider(self, spider):
        pass
    def process_item(self, item, spider):
        # print 'wowowoowowoow'
        # downLoadUrl = item['avatarUrl']
        self.db.qsbk.insert(dict(item))
        # self.dbconn.in
        return item