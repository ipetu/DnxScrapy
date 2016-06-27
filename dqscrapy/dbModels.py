#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/27
import datetime
from mongoengine import *
from settings import dbconn
class ProxyModel(Document):
    """
    代理Ip地址信息存储表
    """
    # proxyIp = StringField(required=True, unique=True)
    # proxyType = StringField(max_length=10)
    proxyList = ListField(required=True,unique=True)
    proxyCtms = DateTimeField(default=datetime.datetime.now, required=True)
    meta = {
        'collection': 'proxyModel',
        # 'indexes': [{'fields': ['proxyIp'], 'unique': True}]
    }

class ProxyModelDispatcher(object):
    @staticmethod
    def saveProxyInfo(mProxyIp = '', mProxyType = ''):
        proxyModel = ProxyModel()
        proxyModel.proxyIp = mProxyIp
        proxyModel.proxyType = mProxyType
        return proxyModel.save()

    @staticmethod
    def saveProxyDict(mProxyList=''):
        proxyModel = ProxyModel()
        proxyModel.proxyList = mProxyList
        return proxyModel.save()
    @staticmethod
    def getProxyInfo():
        return ProxyModel.objects().first()
