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
        if len(item.keys()) == 1:    #存的是content
            try:
                os.chdir("/home/dyh/data/credit11315/detailUrl")
                with open(spider.writeInFile,"a") as f:
                    f.write(item["content"])
            except Exception,e:
                log.msg("content pipeline error_info=%s"%e, level=log.ERROR)
        else:
            for key in item.iterkeys():
                try:
                    os.chdir("/home/dyh/data/credit11315/detailUrl")
                    with open('detailInfoScrapy_'+key,"a") as f:
                        f.write(item[key]+"\n")
                except Exception,e:
                    log.msg("DetailInformation(Item) pipeline error_info=%s"%e, level=log.ERROR)
