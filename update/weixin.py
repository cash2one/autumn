# import requests
#
# url = 'http://weixin.sogou.com/weixin?type=2&query=%E4%B8%AD%E8%BF%9C%E7%B3%BB&ie=utf8&_sug_=y&_sug_type_=1'
# headers = {
#     'Host': 'weixin.sogou.com',
#     'Referer': 'http://weixin.sogou.com/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
# }
#
# r = requests.get(url, timeout=30)
# print r.content

import time
from random import randint
from clean_index import CacheTest


class Test2(object):
    def __init__(self):
        self.t = CacheTest()
        cache = self.t.__class__.cache
        print 'id 2:', id(self.t), id(cache), len(cache)

    def add(self):
        for d in range(111, 120):
            self.t.__class__.cache.add(d)
            time.sleep(randint(1, 3))
            print d, len(self.t.__class__.cache)


if __name__ == '__main__':
    Test2().add()









