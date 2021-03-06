#!usr/bin/env python
#coding: utf-8
from scrapy import Selector
from scrapy import log
import HTMLParser

def fundation_info_extract(response):
    """
    用于提取第一部分：企业信用档案
    """
    sel = Selector(text=response.body)
    xpath_result = [response.url[7:15]] 
    #存xpath提取出来的信息,[response.url[7:15]]为公司的id
    keywords_list = ['注册资金','传真电话','主权商标','经营商标',
    '所在区域','详细地址','主营产品']
    xpath_syn = [u"//b[text()='%s']/../\
                following-sibling::td[1]\
                /text()"%i for i in keywords_list]
    xpath_syn.append(u"//b[text()='单位名称']/../\
            following-sibling::td[1]//a/text()")
    xpath_syn.append(u"//img[@alt='法定代表人']/@src")
    html_parser = HTMLParser.HTMLParser()
    clue = '&nbsp;&nbsp;&nbsp;&nbsp;'
    newclue = html_parser.unescape(clue)
    x_te = u"//span[text()='%s']/../../\
            following-sibling::td[1]/text()"%newclue
    xpath_syn.append(x_te)   #行业
    xpath_syn.append(u"//b[text()='商务网址']/../\
                following-sibling::td[1]/a/@href")
    xpath_syn.append(u"//b[text()='联系电话']/../\
            following-sibling::td[1]/img/@src")

    for i in xpath_syn:
        tmp_x = sel.xpath(i).extract()
        if len(tmp_x) == 0:
            xpath_result.append("")
        elif len(tmp_x) == 1:
            xpath_result.append(tmp_x[0].strip())
        else:
            xpath_result.append("|".join([str(i).strip()\
             for i in tmp_x]))
            log.msg("twomore %s url=%s"%("|".join([str(i).strip()\
             for i in tmp_x]), response.url),level=log.INFO)
    return "\001".join(xpath_result)

