#!usr/bin/env python
#coding: utf-8
from scrapy import Selector
from scrapy import log
def extract_combine_JCXX(response):
    """
    提取监管信息（如http://00225516.11315.com/）
    """
    sel = Selector(text=response.body)
    xpath_result = [response.url[7:15]] 
    #存xpath提取出来的信息,[response.url[7:15]]为公司的id
    keywords1 = ['企业法人营业执照',
    '组织机构代码','税务登记证','银行开户许可证',
    '第三方征信认证']
    xpath_syn1 = [u"//a[text()='%s']/@href"%i for i in keywords1]
    for i in xpath_syn1:
    #提取企业法人营业执照，组织机构
        tmp = sel.xpath(i).extract()
        if len(tmp) == 0:
            xpath_result.append("")
        elif len(tmp) == 1:
            xpath_result.append("http://00225516.11315.com"+tmp[0].strip())
        else:
            log.msg("error for_JCXX xpath_syn1 xpath_result=%s\
                "%"\001".join(xpath_result), level=log.ERROR)

    keywords = ['1-2.质量检查信息','1-3.行政许可资质',\
    '1-4.行政监管信息','1-5.商标/专利/著作权信息',\
    '1-6.人民法院的判决信息','1-7.人民法院判定的被执行人信息',\
    '1-8.人民法院核定的失信被执行人信息']
    # xpath_syn = [u"//a[text()='%s']/ancestor::div[@class=\
    # 'f-cb bdsolid']/div"%i for i in keywords] #xpath语句
    xpath_syn = [u"//a[text()='%s']/../../div"%i for i in keywords] #xpath语句
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