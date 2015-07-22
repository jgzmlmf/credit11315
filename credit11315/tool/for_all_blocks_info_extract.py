#!usr/bin/env python
#coding: utf-8
from scrapy import Selector
from scrapy import log

def block_info_extract(response, keywords_list):
    """
    提取如http://00225516.11315.com/上 行业评价信息，
    媒体评价信息等块信息
    """
    sel = Selector(text=response.body)
    xpath_result = [response.url[7:15]] 
    #存xpath提取出来的信息,[response.url[7:15]]为公司的id
    xpath_syn = [u"//a[text()='%s']/../../div"%i for i in keywords_list] #xpath语句
    for i in xpath_syn:
        raw_re = sel.xpath(i)
        check_total = raw_re.xpath("./a[1]/text()").extract() 
        #查看是否有信息,如是check_total为空，说明没有信息
        check_a = raw_re.xpath("./a")
        #查看总信息是否有分类 ，如果a标签的数量大于1则说明有分类

        if len(check_total) == 0:
            #如果总信息都为0，则直接返回0|0.......
            xpath_result.append("|".join(["0" for i in xrange(0,len(check_a))])+"|") 
            #最后一个"|"是用来隔开url
        elif len(check_a) == 1:
            #如果只有总信息，则直接将信息个数和url拼接
            all_JCXX = check_total[0].strip()
            all_JCXX_url = check_a.xpath("./@href").extract()[0]
            all_JCXX_url = "http://00225516.11315.com" + all_JCXX_url
            xpath_result.append(str(all_JCXX) + "|" + all_JCXX_url)
        else:
            #如果有总信息，且下面有子信息，则迭代将子信息提取出来
            info_me = []
            all_JCXX_url = check_a.xpath("./@href").extract()[0]
            all_JCXX_url = "http://00225516.11315.com" + all_JCXX_url
            for i in xrange(1, len(check_a)+1):
                s = "./a[%s]/text()" %str(i)
                ex_out = raw_re.xpath(s).extract()
                if len(ex_out) == 0:
                    info_me.append("0") #如是a节点没有元素，则加入""
                else:
                    info_me.append(ex_out[0].strip())
            xpath_result.append("|".join(info_me) + "|" + all_JCXX_url)
    return "\001".join(xpath_result) #将个元素用"\001"结合    