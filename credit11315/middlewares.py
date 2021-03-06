# -*- coding: utf-8 -*-

import os
import re
import time
import socket
import base64
import random
from scrapy import log
from credit11315.utils import _default_redis
from scrapy.exceptions import CloseSpider, IgnoreRequest
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from scrapy.xlib.tx import ResponseFailed


class ForbbidenResponseError(Exception):
    """forbbiden response error
    """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        if self.value:
            return repr(self.value)
        else:
            return 'ForbbidenResponseError'

class UnknownResponseError(Exception):
    """未处理的错误"""
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        if self.value:
            return repr(self.value)
        else:
            return 'UnknownResponseError'


class ShouldNotEmptyError(Exception):
    """返回不应该为空，但是为空了，在spider里抛出"""
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        if self.value:
            return repr(self.value)
        else:
            return 'ShouldNotEmptyError'

class RecordSpiderErrorMiddleware(object):
    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
            ConnectionRefusedError, ConnectionDone, ConnectError,
            ConnectionLost, TCPTimedOutError, ResponseFailed,
            IOError, UnknownResponseError, ForbbidenResponseError)

    def __init__(self,proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, proxy_ip_punish):
        self.redis = _default_redis(proxy_redis_host, proxy_redis_port)
        self.proxy_redis_key = proxy_ip_redis_key
        self.proxy_ip_punish = proxy_ip_punish

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_ip_redis_key = settings.get('PROXY_IP_REDIS_KEY', None)
        proxy_redis_host = settings.get('REDIS_HOST', None)
        proxy_redis_port = settings.get('REDIS_PORT', None)
        proxy_ip_punish = settings.get('PROXY_IP_PUNISH', None)
        return cls(proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, \
                proxy_ip_punish)

    def _record(self, response, reason, spider):
        request = response.request
        log.msg(format="undown_personid %(request)s: %(reason)s %(headers)s %(ip)s",
                level=log.ERROR, spider=spider, request=request, reason=reason,\
                        headers=request.headers,ip=request.meta['proxy'])
        proxy_ip = request.meta['proxy']
        self.redis.zincrby(self.proxy_redis_key, proxy_ip, amount=self.proxy_ip_punish/2)  #对因引起对方服务器注意的ip，其惩罚值减半
        return []

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return [self._record(response, exception, spider)]



class ProxyMiddleware(object):
    # overwrite process request
    def __init__(self, proxy_ip_file, proxy_from_redis, proxy_ip_redis_key, proxy_redis_host, proxy_redis_port):
        self.proxy_from_redis = proxy_from_redis
        if not proxy_from_redis:
            with open(proxy_ip_file) as f:
                self.proxy_ips = []
                for line in f:
                    self.proxy_ips.append(line.strip())
                self.proxy_ips_length = len(self.proxy_ips)
        else:
            self.redis = _default_redis(proxy_redis_host, proxy_redis_port)
            self.proxy_redis_key = proxy_ip_redis_key

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_ip_file = settings.get('PROXY_IP_FILE', None)
        proxy_from_redis = settings.get('PROXY_FROM_REDIS', None)
        proxy_ip_redis_key = settings.get('PROXY_IP_REDIS_KEY', None)
        proxy_redis_host = settings.get('REDIS_HOST', None)
        proxy_redis_port = settings.get('REDIS_PORT', None)
        return cls(proxy_ip_file, proxy_from_redis, proxy_ip_redis_key, proxy_redis_host, proxy_redis_port)

    def process_request(self, request, spider):
        if self.proxy_from_redis:
            # 从效果最好的20个IP中随即选取一个IP
            rs = self.redis.zrange(self.proxy_redis_key, 0, 49)
            rs_length = len(rs)
            if rs_length:
                randomidx = random.randint(0, rs_length - 1)
                proxy_ip_port = rs[randomidx]
            else:
                proxy_ip_port = "http://111.13.12.202"
            # 每访问一次，该ip的计数器+1
            self.redis.zincrby(self.proxy_redis_key, proxy_ip_port, amount=1)
        else:
            # Set the location of the proxy
            randomidx = random.randint(0, self.proxy_ips_length-1)
            proxy_ip_port = self.proxy_ips[randomidx]  # "http://111.13.12.202" # "http://218.108.242.124:8080"
            print proxy_ip_port, "middlewares proxy"
        request.meta['proxy'] = proxy_ip_port

        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"

        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass


class IgnoreHttpError(IgnoreRequest):
    """A non-200 response was filtered
    """
    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(IgnoreHttpError, self).__init__(*args, **kwargs)

class Not200Middleware(object):
    """处理状态码不是200的情况
    """
    def __init__(self,proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, proxy_ip_punish):
        self.redis = _default_redis(proxy_redis_host, proxy_redis_port)
        self.proxy_redis_key = proxy_ip_redis_key
        self.proxy_ip_punish = proxy_ip_punish

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_ip_redis_key = settings.get('PROXY_IP_REDIS_KEY', None)
        proxy_redis_host = settings.get('REDIS_HOST', None)
        proxy_redis_port = settings.get('REDIS_PORT', None)
        proxy_ip_punish = settings.get('PROXY_IP_PUNISH', None)
        return cls(proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, \
                proxy_ip_punish)

    def process_spider_input(self, response, spider):
        if response.status != 200:
            raise IgnoreHttpError(response, 'not 200, Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        request = response.request
        if isinstance(exception, IgnoreHttpError):
            log.msg(
                    format="Ignoring response.request %(response)r: not 200 %(reason)s,%(headers)s,\
                            %(ip)s",
                    level=log.ERROR,
                    response=request,
                    reason = exception,
                    headers = request.headers,
                    ip = request.meta['proxy']
            )
            proxy_ip = request.meta['proxy']
            self.redis.zincrby(self.proxy_redis_key, proxy_ip, amount=self.proxy_ip_punish/2)  #对因引起对方服务器注意的ip，其惩罚值减半

            return []


class DownloadTimeoutRetryMiddleware(object):
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
            ConnectionRefusedError, ConnectionDone, ConnectError,
            ConnectionLost, TCPTimedOutError, ResponseFailed,
            IOError)

    def __init__(self,proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, proxy_ip_punish):
        self.redis = _default_redis(proxy_redis_host, proxy_redis_port)
        self.proxy_redis_key = proxy_ip_redis_key
        self.proxy_ip_punish = proxy_ip_punish

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_ip_redis_key = settings.get('PROXY_IP_REDIS_KEY', None)
        proxy_redis_host = settings.get('REDIS_HOST', None)
        proxy_redis_port = settings.get('REDIS_PORT', None)
        proxy_ip_punish = settings.get('PROXY_IP_PUNISH', None)
        return cls(proxy_ip_redis_key, proxy_redis_host, proxy_redis_port, \
                proxy_ip_punish)

    def _retry(self, request, reason, spider):
        log.msg(format="undown_personid %(request)s : %(reason)s,%(headers)s,\
                %(ip)s",
                level=log.ERROR, request=request, reason=reason, headers=request.headers,\
                        ip=request.meta['proxy'])

        raise IgnoreRequest

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            proxy_ip = request.meta['proxy']
            self.redis.zincrby(self.proxy_redis_key, proxy_ip, amount=self.proxy_ip_punish)
            return self._retry(request, exception, spider)
