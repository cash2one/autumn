# -*- coding: utf-8 -*-

from crawler import BaseDownloadHtml
from pyquery import PyQuery


def mfc_func(typ):
    datas = []
    known = {'A': 0, 'B': 1, 'C': 2}

    html = BaseDownloadHtml().get_html('http://i.paizi.com/', encoding=True)
    document = PyQuery(html[0])

    for node in document('.c03-1-1').eq(known.get(typ)).items('li'):
        datas.append(node.text())
    return typ, datas


class Auto(object):
    def __init__(self, *args):
        pass

    def __enter__(self):
        return 123

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'Auto is exit.'


def auto(using=None):
    if callable(using):
        return Auto(using)
    else:
        return Auto()


import time


class Slate(object):
    """ 存储一个字符串和一个变更log，当Pickle时会忘记它的值"""

    def __init__(self, value):
        self.value = value
        self._last_change = time.asctime()
        self.history = {}

    def change(self, new_value):
        # 改变值，提交最后的值到历史记录
        self.history[self.last_change] = self.value
        self.value = new_value
        self.last_change = time.asctime()

    def print_changes(self):
        print 'Changelog for Slate object:'
        for k, v in self.history.items():
            print '%st -> %s' % (k, v)

    def __getstate__(self):
        # 故意不返回self.value 或 self.last_change.
        # 当unpickle，我们希望有一块空白的"slate"
        print 'now get state'
        ddct = self.__dict__
        print ddct
        return ddct

    def __setstate__(self, state):
        # 让 self.history = state 和 last_change 和 value被定义
        print 'set state:', state
        print 'ff:', self.__dict__
        print self.value
        print self._last_change
        print self.history


import cPickle as Pickle
st = Slate(100)
p = Pickle.dumps(st)
print '-' * 50
print st
print '@' * 50
print p
print '-' * 50

up = Pickle.loads(p)
print up
print up.print_changes()
