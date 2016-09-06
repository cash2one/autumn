# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import re
import time
import pinyin
from .. import download
from pyquery import PyQuery
from crawler.sipo.sipo_post import form_data
from eggs.db.mongodb import Mongodb
from multiprocessing.dummy import Pool as ThreadPool


class Sipo(object):
    def __init__(self, typ):
        self._typ = typ
        self._sipo_datas = []
        self._sipo_form = form_data.get_form_data(self._typ)
        self._mongodb = Mongodb('192.168.0.223', 27017, 'py_crawl', 'sipo')

    def extract(self, page):
        checked = lambda t: re.compile(r'\(\d{4}\.\d\d\)', re.S).search(t)
        self._sipo_form['pageNow'] = str(page)
        html_pyq = download.RequestHtml().get_html('http://epub.sipo.gov.cn/patentoutline.action', self._sipo_form)
        document = PyQuery(html_pyq)

        for each_node in document.items('.cp_linr'):
            each_node.remove('a')

            data = {'tit': each_node('h1').text(), 'type': self._typ}
            data.update(self.initial_value(each_node('.cp_jsh').text()))  # obtain zhaiyao to being key and value

            for k, node_li in enumerate(each_node('.cp_linr > ul > li').items()):
                if node_li('li').length == 1:
                    data.update(self.initial_value(node_li.text()))
                else:
                    # handle to multi elements of li tag, sometimes content of child li tag is its parents.
                    flh_flag = False  # assure whether have multi flh, default yes.
                    parent_node_li_text = ''
                    for child_li in node_li.items('li'):
                        if child_li('li').length > 1:
                            flh_flag = True
                            parent_node_li_text += child_li.remove('li').text()
                        else:
                            if flh_flag:
                                flh_flag = False
                                child_li_text = child_li.text()
                                if checked(child_li_text):
                                    # `flh_flag` is true, judge `parent_node_li_text` whether has `flh`,
                                    parent_node_li_text += child_li_text
                                else:
                                    # and must deal with `child_li_text` to update when hasn't child `flh`
                                    data.update(self.initial_value(child_li_text))
                                data.update(self.initial_value(parent_node_li_text))
                            else:
                                data.update(self.initial_value(child_li.text()))

            self._sipo_datas.append(data)

    @staticmethod
    def initial_value(string):
        if not string.strip():
            return {}

        key_value = lambda t: re.compile(r'(.*?)：(.*)', re.S).findall(t)
        try:
            key, value = key_value(string)[0]
            init_py = pinyin.get_initial(key, delimiter='')

            if init_py == 'sqr':
                if pinyin.get(key, delimiter='').endswith('ren'):
                    init_py = '_'.join((init_py, 'person'))
                else:
                    init_py = '_'.join((init_py, 'day'))
            return dict(((init_py, value), ))
        except IndexError:
            pass
        return {}

    def insert_mongo(self, iterable):
        pool = ThreadPool(8)
        pool.map(self.extract, iterable)
        pool.close()
        pool.join()

        # now insert to mongodb at 192.168.0.233
        for mon_data in self._sipo_datas:
            self._mongodb.insert(mon_data)
        del self._sipo_datas[:]

    def main(self):
        unit = 10
        div, mod = divmod(int(self._sipo_form['num' + self._typ.upper()]), 10)
        pages_list = range(1, div + (mod and 1) + 1)
        pagination = len(pages_list) / unit + ((len(pages_list) % unit) and 1)
        dummy_pages_list = [pages_list[p * unit: (p + 1) * unit] for p in range(pagination)]

        for k, dummy_page in enumerate(dummy_pages_list):
            print '\t%s: %s' % (self._typ, dummy_page)
            print 'Now executing [ {1}:{0}] times, per 10 * 10 numbers'.format(k + 1, self._typ)
            self.insert_mongo(dummy_page)
            print '->>>[ {1}: {0} ] times execute is ok, will sleeping 35seconds.\n'.format(k + 1, self._typ)
            time.sleep(25)


def multi_type_sipo(typ):
    Sipo(typ).main()

if __name__ == '__main__':
    sipo = Sipo('fmgb')
    # sipo = Sipo('syxx')
    sipo.main()

    # pools = ProcessPool(2)
    # pools.map(multi_type_sipo, ('syxx', 'fmgb'))
    # pools.close()
    # pools.join()



