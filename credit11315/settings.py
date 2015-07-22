# -*- coding: utf-8 -*-

# Scrapy settings for credit11315 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'credit11315'

SPIDER_MODULES = ['credit11315.spiders']
NEWSPIDER_MODULE = 'credit11315.spiders'

DEFAULT_ITEM_CLASS = 'credit11315.items.Credit11315Item'
ITEM_PIPELINES=['credit11315.pipelines.Credit11315Pipeline']

LOG_FILE = "/home/dyh/data/credit11315/infoDetail/log"

#==============================================================
#form guba_redis

# 不需要默认的180秒,更多的机会留给重试
# The amount of time (in secs) that the downloader will wait before timing out, Default: 180.
DOWNLOAD_TIMEOUT = 180


SPIDER_MIDDLEWARES = {
    # Filters out Requests for URLs outside the domains covered by the spider.
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,

    # Populates Request Referer header, based on the URL of the Response which generated it.
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,

    # Filters out requests with URLs longer than URLLENGTH_LIMIT
    'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': None,

    # DepthMiddleware is a scrape middleware used for tracking the depth of 
    # each Request inside the site being scraped. It can be used to limit 
    # the maximum depth to scrape or things like that.
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,

    # Filter out unsuccessful (erroneous) HTTP responses so that spiders 
    # don’t have to deal with them, which (most of the time) imposes an overhead, 
    # consumes more resources, and makes the spider logic more complex.
    # According to the HTTP standard, successful responses are those whose status codes are in the 200-300 range.
    # If you still want to process response codes outside that range, you can specify which response codes the spider 
    # is able to handle using the handle_httpstatus_list spider attribute or HTTPERROR_ALLOWED_CODES setting.
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': None, # 50,

    # handle 403 forbidden error
    'credit11315.middlewares.Forbbiden403Middleware': 48,

    # handle 302 deleted error
    'credit11315.middlewares.Redirect302Middleware': 49,

    # retry forever middleware
    'credit11315.middlewares.RetryForeverMiddleware': 930,

    # retry 3 times middleware
    'credit11315.middlewares.RetryErrorResponseMiddleware': 940
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'credit11315.rotate_useragent.RotateUserAgentMiddleware' :400,
    # this middleware filters out requests forbidden by the robots.txt exclusion standard.
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': None,

    # This middleware authenticates all requests generated from certain spiders using Basic 
    # access authentication (aka. HTTP auth).
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': None,

    # proxy start
    'credit11315.middlewares.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    # proxy end

    # This middleware sets the download timeout for requests specified in the DOWNLOAD_TIMEOUT setting.
    'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,

    # handle downloadtimeout error
    'credit11315.middlewares.DownloadTimeoutRetryMiddleware': 375,

    # Middleware that allows spiders to override the default user agent.
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,

    # A middlware to retry failed requests that are potentially caused by temporary problems such as 
    # a connection timeout or HTTP 500 error.
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None, # 500,

    # This middleware sets all default requests headers specified in the :setting:`DEFAULT_REQUEST_HEADERS` setting.
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': None,

    # This middleware handles redirection of requests based on meta-refresh html tag.
    'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': None, # 580,

    # This middleware allows compressed (gzip, deflate) traffic to be sent/received from web sites.
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,

    # this middleware handles redirection of requests based on response status.
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,

    # This middleware enables working with sites that require cookies, such as 
    # those that use sessions. It keeps track of cookies sent by web servers, 
    # and send them back on subsequent requests (from that spider), just like web browsers do.
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,

    # This middleware adds support for chunked transfer encoding
    'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,

    # Middleware that stores stats of all requests, responses and exceptions that pass through it.
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,

    # This middleware provides low-level cache to all HTTP requests and responses. 
    # It has to be combined with a cache storage backend as well as a cache policy.
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': None
}

# If enabled, Scrapy will wait a random amount of time (between 0.5 and 1.5 * DOWNLOAD_DELAY)
# while fetching requests from the same website.
RANDOMIZE_DOWNLOAD_DELAY = True

REFERER_ENABLED = False # disable RefererMiddleware

# retry middleware settings
RETRY_TIMES = 3 # RetryMiddleware Maximum number of times to retry, in addition to the first download. RetryErrorResponseMiddleware 重试次数
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]

# RetryForeverMiddleware
RETRY_INIT_WAIT = 1 # 第一次重试等待1s
RETRY_STABLE_TIMES = 100 # 重试100次之后WAIT不再增加
RETRY_ADD_WAIT = 1 # 每次重试后增加的等待秒数

PROXY_FROM_REDIS = False 
# Proxy ip list file
PROXY_IP_FILE = './credit11315/proxy_ips.txt'
PROXY_IP_REDIS_KEY = 'credit11315_proxy_ips:sorted_set'
PROXY_IP_PUNISH = 10000 # 每次IP访问失败增加的等待时间

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# ======================================================

# ======================================================
#detail_info_scrapy.py的配置文件
host = 'localhost'    #redis_host
port = 6379           #redis_port
# ======================================================

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'credit11315 (+http://www.yourdomain.com)'
