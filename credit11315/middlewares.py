#coding: utf-8

import random
import os
os.chdir("/home/dyh/spiders/credit11315/credit11315")

class ProxyMiddleware(object):
    # overwrite process request
    def __init__(self):
        with open("proxy_ips.txt") as f:
            self.proxy_ips = []
            for line in f:
                self.proxy_ips.append(line.strip())
            self.proxy_ips_length = len(self.proxy_ips)


    def process_request(self, request, spider):
        if self.proxy_ips_length:
            randomidx = random.randint(0, self.proxy_ips_length - 1)
            proxy_ip_port = self.proxy_ips[randomidx]
        else:
            proxy_ip_port = "http://111.13.12.202"
        print proxy_ip_port, "post ip"
        request.meta['proxy'] = proxy_ip_port