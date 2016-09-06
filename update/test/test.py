# -*- coding: utf-8 -*-

import sys
import requests
import chardet
from pyquery import PyQuery


def tracer(func):  # State via enclosing scope and func attr
    def wrapper(*args, **kwargs):  # calls is per-function, not global
        wrapper.calls += 1
        print('call %s to %s' % (wrapper.calls, func.__name__))
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


class CBB(object):
    def __init__(self):
        self._name = 'abc'

    def __getattr__(self, name):
        print 'name:', name
        return 1230

    def method(self, *args):
        print 'method:', self, args


@tracer
def eggs(x, y):
    print x, y


def big_data():
    import heapq
    import time
    from random import randint

    def generate_big_data():
        num = 100000000
        for _ in xrange(num):
            yield randint(1, num * 2)

    s = time.time()
    iteror = generate_big_data()

    print 'dene data:', time.time() - s

    st = time.time()
    big = heapq.nlargest(10, iteror)
    ed = time.time()
    print ed - st, big


if __name__ == '__main__':
    big_data()
