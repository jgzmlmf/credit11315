#!usr/bin/env python
#coding: utf-8

"""
从11315全国企业征信系统http://www.11315.com/上
爬取企业信息
"""
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import log
from scrapy import signals
from scrapy import Selector
from scrapy.exceptions import DontCloseSpider
import sys
from credit11315.items import *
from credit11315.middlewares import UnknownResponseError, ForbbidenResponseError
from credit11315.tool.for_ominated_strip import for_ominated_data
from credit11315.tool.for_JCXX import extract_combine_JCXX
from credit11315.tool.for_all_blocks_info_extract import block_info_extract
from credit11315.tool.for_fundation_info_extract import fundation_info_extract
import HTMLParser
import redis
import urllib2


reload(sys)
sys.setdefaultencoding("utf-8")

class GetDetailInfo(Spider):
    """
    从redis上读取url，并提取企业的信息
    """
    name = 'detailinfo'
    redis_key = "all_detail_url"
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    def set_crawler(self, crawler):
        super(GetDetailInfo, self).set_crawler(crawler)
        self.setup_redis()

    def setup_redis(self):
        """
        1,连接redis
        2,绑定signals.spider_idle信号
        """
        print "setup_redis work"
        self.server = self.from_settings() #连接服务器
        self.crawler.signals.connect(self.spider_idle, \
            signal=signals.spider_idle)  #绑定信号
        #self.crawler.signals.connect(self.item_scraped, \
        #    signal=signals.item_scraped)     #速度太慢
        self.crawler.signals.connect(self.request_scheduled,\
                signal=signals.request_scheduled)

    def from_settings(self):
        print "from_settings work"
        # REDIS_URL 较 host/port 有更高的优先级.返回的是redis客户端连接实例
        return redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_request()
        raise DontCloseSpider

    def schedule_next_request(self):
        """Schedules a request if available"""
        req = self.next_request()
        if req:
            #time.sleep(60) #for test redis
            self.crawler.engine.crawl(req, spider=self)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        url = self.server.lpop(self.redis_key)
        if url:
            return self.make_requests_from_url(url)

    def item_scraped(self, *args, **kwargs):
        """Avoids waiting for the spider to  idle before scheduling the next request"""
        self.schedule_next_request()

    def request_scheduled(self, *args, **kwargs):
        self.schedule_next_request()

    def parse(self, response):
        """
        解析
        """
        sel = Selector(text=response.body)
        print len(sel.xpath(u"//b[text()='单位名称']"))!= 0, "parse 条件"
        log.msg("parse 条件=%s"%str(len(sel.xpath(u"//b[text()='单位名称']")) != 0), level=log.INFO)
        if (len(sel.xpath(u"//b[text()='单位名称']")) != 0): #判别是否为要输入验证码
            pass
        else:
            log.msg("code=%s,  %s"%(str(response.status),response.body), level=log.INFO)
            raise UnknownResponseError
        #========================================================
        """
        第一部分：企业信用档案
        """
        item = DetailInformation()
        item['basic_info'] = fundation_info_extract(response)
        #========================================================
        #========================================================
        """
        第一部分 政府监管信息
        """
        item['regulatory_info'] = extract_combine_JCXX(response)
        #========================================================
        #========================================================
        """
        第三部分 行业评价信息
        """
        keywords_list = ['2-1.体系/产品/行业认证信息',
            '2-2.行业协会(社会组织)评价信息',\
            '2-3.水电气通讯等公共事业单位评价']
        item['envaluated_info'] = block_info_extract(response,\
            keywords_list)
        #========================================================
        """
        第四部分 媒体评价信息
        """
        keywords_list = ['3-1.媒体评价信息']
        item['media_env'] = block_info_extract(response, keywords_list)
        #========================================================
        """
        第五部分 金融信贷信息
        """
        #url = 'http://www.11315.com/\
        #getTradeLendingCount?companyId=%s'%response.url[7:15]
        #header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
        #  'Referer':response.url}
        #req = urllib2.Request(url=url, headers=header)
        #xtml = urllib2.urlopen(req)
        #Nums = xtml.read()
        #print Nums, "this is Nums"
        #Nums = eval(Nums).split(",")
        #print Nums, "this is anothor Nums"
        #total = str(sum([int(i) for i in Nums]))
        #Nums.insert(0, total)  #在头部插入
        #if total == '0':
        #    t_url = ""
        #else:
        #    t_url = sel.xpath(u"//script").re(ur"html\(\'<a href=\"([\w\W]*?)\"")[0]
        #Nums.append(t_url)
        #Nums_re = "|".join(Nums)
        keywords_list = ['4-2.民间借贷评价信息']
        item["credit_fin"] = block_info_extract(response, keywords_list)
        #=======================================================
        """
        第六部分 企业运营信息
        """
        #keywords_list = ['5-3.水电煤气电话费信息',
        #'5-4.纳税信息']                          #要么运行js,要么模拟请求，破网站，就两行数据至于吗
        #item['operation_info'] = block_info_extract(response, keywords_list)
        #========================================================
        """
        第七部分 市场反馈信息
        """
        keywords_list = ['6-1.消费者评价信息',
        '6-2.企业之间履约评价','6-3.员工评价信息',
        '6-4.其他']
        item['feedback_info'] = block_info_extract(response, keywords_list)
        #========================================================
        return item
        #else: 
        #    print "raise unknownresponseError in spider", response.request.meta
        #    #raise UnknownResponseError
        #    #raise ForbbidenResponseError("work or no nnnnnn")
        #    request = response.request
        #    retryreq = request.copy()
        #    retryreq.dont_filter = True
        #    log.msg("UnknowResponseError %s"%response.body, level=log.INFO)
        #    yield retryreq










