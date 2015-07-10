#coding: utf-8

import pickle

class xpath(object):
    """
    extract data by xpath
    """
    def classiUrl_xpath(self,response):
        """
        extract url of all classi 
        from response of http://www.11315.com/rankAllList
        """
        sel = response.selector
        all_url = {}   #
        classi = sel.xpath(u"//dl[@class='sortdl']/dt/text()").extract()
        xpath_s = u"//dt[text()='{tag}']/following-sibling::*\
            /a/@href"
        all_url = {}
        for i in te:
            # print 'fir', i
            xpath_s = u"//dt[text()='{tag}']/following-sibling::*\
                    /a/@href"
            xpath_s = xpath_s.format(tag=unicode(i))
            all_url[i[:-1]] = sel.xpath(xpath_s).extract()

        return pickle.dump(all_url)
