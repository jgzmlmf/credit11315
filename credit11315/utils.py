# -*- coding: utf-8 -*-

import re
import os
import md5
import time
import redis
import errno
import socket
from datetime import datetime


MONGOD_HOST = 'localhost'
MONGOD_PORT = 27017
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def now_datestr():
    return time.strftime('%m-%d', time.localtime(time.time()))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise

def gen_key(key):
    """Given a string key it returns a long value,
       this long value represents a place on the hash ring.
       md5 is currently used because it mixes well.
    """
    m = md5.new()
    m.update(key)
    return long(m.hexdigest(), 16)


def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port, db)

def get_pid():
    return os.getpid()

def get_ip():
    host_ip = 'Unknown'
    names, aliases, ips = socket.gethostbyname_ex(socket.gethostname())
    for ip in ips :
        if not re.match('^192', ip) and not re.match('^172', ip):
            host_ip = ip

    return host_ip

