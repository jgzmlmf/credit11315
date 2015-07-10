# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
import os
os.chdir("E:/DLdata")
class Credit11315Pipeline(object):
    def process_item(self, item, spider):
        try:
            with open("all_url","a") as f:
                f.write(item['content'])
        except Exception,e:
            log.msg("error pipeline", level=log.ERROR)
