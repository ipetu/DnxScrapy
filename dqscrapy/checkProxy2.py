#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Liuwf on 16/6/27
'''
检测代理 IP 的响应时间（ping），验证proxy是否可用
检测代理 IP 是否返回数据，验证Ping通是否可用
'''

import os
import urllib2
import random
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

PROXY_LIST = [
    {'http': "http://183.60.6.172:8080"},
    {'http': "http://120.202.249.197:80"}
    # {'http': "http://77.70.29.176:81"},
    # {'http': "http://41.223.119.156:3128"},
    # {'http': "http://188.138.247.175:8080"},
    # {'https': "https://217.33.193.179:3128"},
    #
    # {'http': "http://221.10.102.199:82"},
    # {'https': "https://119.188.94.145:80"},
    # {'https': "https://120.236.148.113:3128"},
    #
    # {'http': "http://183.209.236.152:8123"},
    # {'http': "http://113.56.149.118:8088"}
]

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]


# 使用代理访问网站 - GET方式实现
def spider_url_by_get(proxy=None):
    url = 'http://www.baidu.com'
    #     url = 'http://localhost:8888/'
    #     url = 'http://localhost/proxy_client/test/test_proxy.php'

    #     proxy = random.choice(PROXY_LIST)
    print 'proxy : ', proxy

    try:
        proxyHandler = urllib2.ProxyHandler(proxy)
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies, proxyHandler, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request(url)

        user_agent = random.choice(USER_AGENT_LIST)
        req.add_header('User-Agent', user_agent)
        data = urllib2.urlopen(req, timeout=10).read()

        dataJson = json.loads(str(data), encoding='utf-8')
        #     dataJson['user_agent'] = str(user_agent)
        #     dataJson['proxy'] = str(proxy)

        data = json.dumps(dataJson)
        print 'spider_url_by_get（） +++++++++ ', data
    except Exception, ex:
        print 'spider_url_by_get（） -------- ', ex


# 使用代理访问网站 - POST方式实现
def spider_url_by_post():
    pass


def ping_ip(ip=None):
    ping_cmd = 'ping -c 2 -W 5 %s' % ip

    #     ping_result = os.system(ping_cmd)
    #     print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
    #
    #     if ping_result == 0:
    #         print 'ping %s ok' % ip
    #         return True
    #     else:
    #         print 'ping %s fail' % ip


    ping_result = os.popen(ping_cmd).read()
    print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)

    if ping_result.find('100% packet loss') < 0:
        print 'ping %s ok' % ip
        return True
    else:
        print 'ping %s fail' % ip


def main():
    for proxy in PROXY_LIST:
        for key in proxy.keys():
            value = proxy.get(key, '')
            ip = value.split("//")[1].split(":")[0].strip()

            if ping_ip(ip):
                spider_url_by_get(proxy)


if __name__ == '__main__':
    main()
