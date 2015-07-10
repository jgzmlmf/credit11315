#coding: utf-8

from scrapy import Spider
from scrapy import log
from scrapy import Request
from credit11315.tool.xpath.xpath import classiUrl_xpath 
from credit11315.items import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Credit11315(Spider):
    """
    从http://www.11315.com/rankAllList上抓取所有行业
    的url并写入到文件中
    """
    name = 'rank'
    start_urls = ['http://www.11315.com/rankAllList']
    writeInFile = 'all_urls_credit11315'
    def parse(self, response):
        """
        doc
        """
        item = Credit11315Item()
        item['content'] = classiUrl_xpath(response)
        if item['content']:
            yield item
        else:
            log.msg("error in parse, nothing returned from\
                classiUrl_xpath", level=log.ERROR)
