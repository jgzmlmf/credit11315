# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
import os
os.chdir("/home/dyh/data/credit11315/detailUrl")
class Credit11315Pipeline(object):
    def process_item(self, item, spider):
        try:
            os.chdir("/home/dyh/data/credit11315/detailUrl")
            with open(spider.writeInFile,"a") as f:
                f.write(item["content"])
        except Exception,e:
            log.msg("error pipeline error_info=%s"%e, level=log.ERROR)
