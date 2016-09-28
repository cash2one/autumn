#!/root/.pyenv/versions/anaconda-2.3.0/bin/python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import re
import os
import sys
import traceback
import time

import urlparse
import requests
import simplejson
import itertools
# from aaa import cache
from pyquery import PyQuery
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from collections import Counter, OrderedDict
from collections import defaultdict
from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient


import importlib
import scrapyd
from eggs.db.mongodb import Mongodb
from eggs.utils.utils import write, md5
# from eggs.utils.xlsx_writer import XlsxWriter
from eggs.utils.xlsx import XlsxReader


path = r'D:/temp/data/'
book_values = []


def update_item_sipo():
    coll = Mongodb('192.168.0.223', 27017, 'py_crawl', 'sipo_typ')
    headers_fmgb = [
        'tit', 'sqgbh(申请公布号)', 'sqgbr(申请公布日)', 'sqh(申请号)', 'sqr_day(申请日)', 'sqr_person(申请人)',
        'fmr(发明人)', 'dz(地址)', 'flh(分类号)', 'zy(摘要)', 'zldljg(专利代理机构)', 'dlr(代理人)', 'yxq(优先权)',
        'PCTjrgjjdr(PCT进入国家阶段日)', 'PCTsqsj(PCT申请数据)', 'PCTgbsj(PCT公布数据)', 'gzwxcbr(更正文献出版日)',
        'swbc(生物保藏)', 'faysq(分案原申请)', 'bgyxq(本国优先权)'
    ]

    headers_syxx = [
        'tit', 'sqggh(授权公告号)', 'sqggr(授权公告日)', 'sqh(申请号)', 'sqr_day(申请日)', 'zlqr(专利权人)',
        'fmr(发明人)', 'dz(地址)', 'flh(分类号)', 'zy(摘要)', 'zldljg(专利代理机构)', 'dlr(代理人)',
        'yxq(优先权)', 'PCTjrgjjdr(PCT进入国家阶段日)', 'PCTsqsj(PCT申请数据)', 'PCTgbsj(PCT公布数据)',
        'gzwxcbr(更正文献出版日)', 'faysq(分案原申请)',  'bgyxq(本国优先权)'
    ]
    open_book_fmgb = XlsxWriter(path + 'sipo_fmgb.xlsx', 'fmgb', headers_fmgb)
    keys_fmsq = [
        'tit', 'sqgbh', 'sqgbr', 'sqh', 'sqr_day', 'sqr_person', 'fmr', 'dz', 'flh', 'zy', 'zldljg',
        'dlr', 'yxq', 'PCTjrgjjdr', 'PCTsqsj', 'PCTgbsj', 'gzwxcbr', 'swbc', 'faysq', 'bgyxq'
    ]
    for k, dct in enumerate(coll.query({'type': 'fmgb'}).sort([('_id', 1)])):
        open_book_fmgb.write([dct.get(key, '') for key in keys_fmsq])
        print 'fmgb:', k
    open_book_fmgb.close()

    open_book_syxx = XlsxWriter(path + 'sipo_syxx.xlsx', 'syxx', headers_fmgb)
    keys_syxx = [
        'tit', 'sqggh', 'sqggr', 'sqh', 'sqr_day', 'zlqr', 'fmr', 'dz', 'flh', 'zy', 'zldljg', 'dlr',
        'yxq', 'PCTjrgjjdr', 'PCTsqsj', 'PCTgbsj', 'gzwxcbr', 'faysq',  'bgyxq'
    ]
    for ks, dct in enumerate(coll.query({'type': 'syxx'}).sort([('_id', 1)])):
        open_book_syxx.write([dct.get(key, '') for key in keys_syxx])
        print 'syxx', ks
    open_book_syxx.close()


def insert_db_from_file_bond():
    def get_secu(code_string):
        secu = re.compile(r'\((\d+)\)').findall(code_string)
        # print 'se:', secu
        return secu[0]

    secu_keys = ['y', 'secu', 'price', 'volu', 'ot']
    coll_in = Mongodb('192.168.0.223', 27017, 'ada', 'base_block_trade')

    with open('d:/temp/bond_data_json.txt') as fd:
        for k, each in enumerate(fd):
            item = each.strip()
            if not item or item.startswith('#'):
                continue

            to_list = []
            for j, s in enumerate(simplejson.loads(item)):
                if j == 1:
                    tt = s.replace('\\28', '(').replace('\\29', ')')
                    to_list.append(tt)
                else:
                    to_list.append(s.decode('unicode-escape'))

            data = dict(zip(secu_keys, to_list))
            data['s'] = data['secu']
            data['secu'] = get_secu(data['secu'])
            data['volu'] = '{0:.2f}'.format(float(data['volu']) * 10000 * 100)
            data['amou'] = '{0:.2f}'.format(float(data['volu']) * float(data['price']))
            data['sale'], data['buy'] = '', ''
            data['typ'] = 'sha_bond'
            # print data
            data.pop('ot')
            coll_in.insert(data)
            # break
            print '{0} ok'.format(k + 1)
    coll_in.disconnect()


def insert_db_from_file_secu():
    def get_secu(code_string):
        secu = re.compile(r'\((\d+)\)').findall(code_string)
        # print 'se:', secu
        return secu[0]

    secu_keys = ['y', 'secu', 'price', 'amou', 'volu', 'buy', 'sale', 'ot']
    coll_in = Mongodb('192.168.0.223', 27017, 'ada', 'base_block_trade')

    with open('d:/temp/secu_data_json.txt') as fd:
        for k, each in enumerate(fd):
            item = each.strip()
            if not item or item.startswith('#'):
                continue

            to_list = []
            for j, s in enumerate(simplejson.loads(item)):
                if j == 1:
                    tt = s.replace('\\28', '(').replace('\\29', ')')
                    to_list.append(tt)
                else:
                    to_list.append(s.decode('unicode-escape'))

            data = dict(zip(secu_keys, to_list))
            data['s'] = data['secu']
            data['secu'] = get_secu(data['secu'])
            data['volu'] = '{0:.2f}'.format(float(data['volu']) * 10000)
            data['amou'] = '{0:.2f}'.format(float(data['amou']) * 10000)
            data['typ'] = 'sha_secu'
            # print data
            data.pop('ot')
            coll_in.insert(data)
            print '{0} ok'.format(k + 1)
    coll_in.disconnect()


def csf_news():
    coll200 = Mongodb('192.168.250.208', 27017, 'news', 'new_keyword_dict')
    coll_csf = Mongodb('192.168.250.208', 27017, 'news', 'csf_dict')

    for k, doc in enumerate(coll200.query(), 1):
        word = doc['word']
        coll_csf.insert({'word': word, 'nat': 0, 'stat': 2, 'w': 1000})
        print k
    coll200.disconnect()
    coll_csf.disconnect()


def csf_dict():
    coll200 = Mongodb('192.168.250.208', 27017, 'news', 'csf_dict')
    ww = '送股实施公告  权益分派  分红派息  分红实施  转增股本 分派 OR 利润分配 OR 分配实施 OR 现金股利 OR ' \
         '现金分红 OR 现金红利 OR 股息派发 NOT 调整非公开股票 NOT 调整发行股份 NOT 预案 NOT 预披露 NOT ' \
         '管理制度 NOT 独立意见 NOT 法律意见书 NOT 预告 NOT 说明会 NOT 提示性公告 NOT 英文版 NOT 提议 ' \
         'NOT 临时公告 NOT 募集资金 NOT 完毕 NOT 调整发行股票价格'

    www = ww.replace('OR', ' ').replace('NOT', ' ')
    words = [w.strip() for w in www.split() if w.strip()]
    for wr in words:
        data = {'stat': 1, 'w': 1010, 'nat': 1, 'word': wr}
        coll200.insert(data)
    coll200.disconnect()


def update_item():
    conceptions = []
    work_book = XlsxReader(path + 'www.xlsx')
    base_keys = ['conp', 'resc', 'cpcd', 'idxcd', 'rel']

    for _k, doc in enumerate(work_book.collection(), 1):
        temp = {}
        temp['conp'] = doc['conp']
        temp['cpcd'] = doc['cpcd']
        temp['resc'] = [s.strip()for s in doc['resc'].split('&')]
        temp['rel'] = [s.strip()for s in doc['rel'].split(';')]
        temp['idxcd'] = [] if not doc['idxcd'].strip() else [doc['idxcd'].strip()]


        cw = []
        for k, vs in doc.iteritems():
            if k not in base_keys:
                cw.extend([v.strip() for v in vs if v.strip()])
        temp['cw'] = cw
        print _k
        conceptions.append(temp)

    print 'read xlsx finished.'
    dicts = defaultdict(list)
    for dox in conceptions:
        dicts[dox['conp']].extend(dox['idxcd'])

    for _temp_data in conceptions:
        conp = _temp_data['conp']
        _temp_data['idxcd'] = dicts[conp]

    coll = Mongodb('192.168.250.208', 27017, 'news', 'news_conp')
    for data in conceptions:
        coll.insert(data)
    coll.disconnect()


def statistics(months=None, weeks=None, days=None):
    if months:
        query_range = str(datetime.now() - timedelta(days=30)).replace('-', '')[:8]
    elif weeks:
        query_range = str(datetime.now() - timedelta(days=7)).replace('-', '')[:8]
    elif days:
        pass

    coll_from = Mongodb('192.168.250.208', 27017, 'news', 'hotnews_analyse')
    coll_to = Mongodb('192.168.250.208', 27017, 'news', 'statistics')

    all_ind = {_ind for _doc in coll_from.query(kwargs={'ind': 1}) for _ind in _doc.get('ind', [])}

    for ind in all_ind:
        counter = Counter()
        query_cond = {'ind': {'$in': [ind]}, 'dt': {'$gte': query_range + '000000'}}

        for doc in coll_from.query(query_cond, {'kw': 1}):
            counter.update(doc.get('kw', []))

        data = {'ind': ind, 'count': counter.most_common(100), 'dt': query_range}
        coll_to.insert(data)
    coll_from.disconnect()
    coll_to.disconnect()


def handle_163_text():
    """ 找出208 sum 字段有影响的文本记录 """
    pattern = re.compile(r'网易财经会赚钱的客户端|网易财经 会赚钱的客户端')
    query_cond = {'url': {'$regex': re.compile(r'163\.com')}, 'ratio': 0}

    coll = Mongodb('192.168.0.223', 27017, 'news_crawl', 'hot_news')
    # print coll.query({'content': {'$regex': re.compile(r'%s' % text)}}).count()
    for k, doc in enumerate(coll.query(query_cond), 1):
        content = doc['content']

        if pattern.search(content) is not None:
            url = doc['url']
            title = doc['title'].split('重点推荐', 1)[0]
            auth = doc['author']
            pub_date = doc['date']
            cat = doc.get('source')
            ratio = doc.get('ratio')

            new_content = pattern.split(content, 1)[0].split('div,h1', 1)[0].strip('#&# ')

            if cat and new_content:
                lines = [url, title, auth, str(pub_date), new_content, cat, str(ratio)]
                write(path + '20151119/', str(pub_date), lines)

            print 'id:', doc['_id'], k
    coll.disconnect()


def remove_by_url():
    """ 删除208 sum 字段有影响的文本记录， 通过 handle_163_text函数产生的文件中的url """
    count = 0
    verbose_dicts = {}
    files_path = 'D:/temp/data/20151119/'
    coll_208 = Mongodb('192.168.250.208', 27017, 'news', 'topnews_analyse')

    for _docs in coll_208.query({'url': {'$regex': re.compile(r'163\.com')}}, {'url': 1}):
        verbose_dicts[_docs['url']] = _docs['_id']

    keys_set = {key for key in verbose_dicts}
    for _c, filename in enumerate(os.listdir(files_path), 1):
        with open(files_path + filename) as fp:
            url = fp.readline().strip()

            if url in keys_set:
                count += 1
                object_id = verbose_dicts[url]
                coll_208.update({'_id': object_id}, setdata={'stat': 0})
                print('Order: {}, count: {}, id: {}'.format(_c, count, object_id))
                time.sleep(0.4)
                # break

    coll_208.disconnect()


host = '192.168.100.20'
port = 27017
coll = Mongodb(host, port, 'opt', 'test')


def temp():
    mapping = {
        '美股新闻': {'美股新闻', 'us_gg', 'us_hy', 'us_hg', 'us_gs', '美股个股', 'us'},
        '基金新闻': {'基金新闻'},
        '新三板': {'新三板'},
        '港股新闻': {'港股新闻', 'hk'},
        'A股新闻': {'公司新闻', '股评新闻', '宏观新闻', ' 宏观新闻', '行业新闻', ' 行业新闻', '热点新闻', 'hjd', 'hot', 'test',
                 '政策新闻', 'hotnews', '私募投资'},
    }
    client = MongoClient('192.168.100.20')
    coll_20 = client.news_crawl.finance_news_all_org

    # cat = coll_20.distinct('source')
    # print '\n'.join(cat)
    for key in mapping:
        values = list(mapping[key])
        print key, coll_20.find({'source': {'$in': values}}).count()
    client.close()


def ktest():
    history_data = defaultdict()
    index_data = defaultdict(dict)
    client = MongoClient('192.168.100.20')
    coll_cons = client.ada.constituent
    coll_hist = client.ada.index_members
    coll_in = client.ada.index_members
    fields = ['p_code', 's_code', 'in_dt', 'out_dt']

    for docs in coll_hist.find():
        _id = docs.pop('_id')
        key = docs['p_code'] + docs['s_code'] + docs['in_dt']
        history_data[key] = [docs['out_dt'], _id]
        index_data[_id] = docs

    print len(history_data)
    for _docs in coll_cons.find():
        _out_dt = _docs['out_dt']
        _key = _docs['p_code'] + _docs['s_code'] + _docs['in_dt']

        value = history_data.get(_key)

        if value:
            if _out_dt and value[0]:
                pass

            if _out_dt and not value[0]:
                r_id = value[1]

                index_data[r_id]['out_dt'] = _out_dt
                coll_in.insert(index_data[r_id])
                pass

            if not _out_dt and value[0]:
                # print '1000:', value[1]
                pass

            if not _out_dt and not value[0]:
                pass
        else:
            _docs.pop('_id')
            coll_in.insert(_docs)
            pass

    client.close()


def index():
    from pymongo import MongoClient
    path = 'D:/temp/index/'
    client_95 = MongoClient('122.144.134.95')
    coll_95 = client_95.ada.index_members_a

    # coll_20.update(query, {'$set': {'stat': 0, 'upt': datetime.now()}})

    for filename in os.listdir(path):
        with open(path + filename) as fp:
            p_code = filename.replace('.txt', '').split('_')[-1]

            for line in fp:
                code = line.strip()
                query = {'cat': 'cnindex', 'p_code': p_code, 's_code': code}
                print p_code, code, coll_95.find(query).count()

                cursor = coll_95.find(query).sort([('in_dt', -1)])

                if cursor.count() >= 2 and cursor[0]['in_dt'] >= '2016-06-21':
                    setdata = {'stat': 0, 'upt': datetime.now()}
                    coll_95.update({'_id': cursor[0]['_id']}, {'$set': setdata})
                    print 100000, p_code, code, cursor[0]['_id']
                    # break

                if cursor.count() == 1:
                    setdata = {'stat': 2, 'upt': datetime.now(), 'out_dt': '20160701', 'sign': '1'}
                    coll_95.update({'_id': cursor[0]['_id']}, {'$set': setdata})
                    print 111111, p_code, code, cursor[0]['_id']
                    # break

    client_95.close()


def remove_otc():
    excel_path = 'D:/test/need_delete.xlsx'
    workbook = XlsxReader(excel_path)
    coll = Mongodb('122.144.134.95', 27017, 'news', 'announcement_otc')

    for ind, doc in enumerate(workbook.collection(_id=str), 1):
        # print doc['_id'], ind

        if ind >= 0:
            print doc['_id'], ind
            coll.update({'_id': ObjectId(doc['_id'])}, setdata={'stat': 0, 'upt': datetime.now()})
        # break

    coll.disconnect()


if __name__ == '__main__':
    # update_item()
    # csf_news()
    # statistics(months=True)

    # handle_163_text()
    # remove_by_url()

    # temp()
    # ktest()
    # index()
    remove_otc()





