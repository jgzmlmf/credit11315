#coding: utf-8

from scrapy import log

def for_ominated_data(data_list, info_list, response):
    """
    有些字段没有数据，所以用“”代替
    """
    if len(data_list) == 0:
        data_list.append("")
    else:
        pass
    try:
        assert len(data_list) == 1, "data_list must be uniqe"
        info_list.append(data_list[0].strip())
    except Exception, e:
        log.msg("error for_omi info=%s, info_list=%s,url=%s"%(e, \
            "|".join(info_list), response.url), level=log.ERROR)
    return info_list
