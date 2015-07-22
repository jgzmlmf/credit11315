# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Credit11315Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = Field()

class DetailInformation(Item):
    """
    企业信用档案部分的信息
    """
    basic_info = Field()
    regulatory_info = Field()
    envaluated_info = Field()
    media_env = Field()
    credit_fin = Field()
    operation_info = Field()
    feedback_info = Field()
