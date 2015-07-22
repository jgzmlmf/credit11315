#!usr/bin/env python
#coding: utf-8

import redis

myRedis = redis.Redis(host='localhost', port=6379)
mypath = "/home/dyh/data/credit11315/detailUrl/uniq_all_detail_url"
f = open(mypath, "r")
i = 0
for line in f:
    myRedis.lpush("all_detail_url", line.strip())
    i = i + 1
    if i>=10:
        break
