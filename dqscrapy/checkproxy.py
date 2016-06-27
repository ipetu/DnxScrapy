#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/27
# coding=utf-8

import urllib2
import urllib
import time
import socket

from dbModels import ProxyModelDispatcher
from proxy import PROXIES, FREE_PROXIES
ip_check_url = 'http://www.qiushibaike.com/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
socket_timeout = 30


# Check proxy
def check_proxy(protocol, pip):
    try:
        proxy_handler = urllib2.ProxyHandler({protocol: pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', user_agent)] #这句加上以后无法正常检测，不知道是什么原因。
        urllib2.install_opener(opener)

        req = urllib2.Request(ip_check_url)
        time_start = time.time()
        conn = urllib2.urlopen(req)
        # conn = urllib2.urlopen(ip_check_url)
        time_end = time.time()
        detected_pip = conn.read()

        proxy_detected = True

    except urllib2.HTTPError, e:
        print "ERROR: Code ", e.code
        return False
    except Exception, detail:
        print "ERROR: ", detail
        return False

    return proxy_detected


def main():
    socket.setdefaulttimeout(socket_timeout)
    protocol = "http"
    proxyModel = ProxyModelDispatcher.getProxyInfo()
    if proxyModel is not None:
        proxyList = proxyModel['proxyList']
        if proxyList is not None and len(proxyList)>0:
            for ip in proxyList:
                ipProt = ip['HTTP']
                proxy_detected = check_proxy(protocol, ipProt)
                if proxy_detected:
                    print (" WORKING: " + ipProt)
                else:
                    print " FAILED: %s " % (ipProt,)


if __name__ == '__main__':
    main()
