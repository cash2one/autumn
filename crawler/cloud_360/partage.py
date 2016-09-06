#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import urllib
import urllib2
import requests
import datetime
import chardet
from time import strftime
from random import randint
from pyquery import PyQuery
from multiprocessing.dummy import Pool as ThreadPool
from crawler.cloud_360.db_handler import log, xlsx_infos, db_insert, comp_infos
from crawler.cloud_360.config import log_normal, log_alexa, log_patent
from crawler.cloud_360.config import db, db_name, table_name_insert


class Partage(object):
    def __init__(self):
        self.__info = re.compile(r'\d+')
        self.__grade = re.compile(r"showHint\('(.*?),(.*?),(.*?)'\);")
        self.__court = re.compile(r"""<span style='color:black(.*?)\)""")

    def downloader(self, url, data=None):
        for _ in range(1, 5):
            req = urllib2.Request(url) if not data else urllib2.Request(url, data)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
            try:
                response = urllib2.urlopen(req, timeout=30.0)
                feed_data = response.read()
                response.close()
                return feed_data
            except Exception as e:
                print 'Web open error:', e, self.__class__.__name__
                time.sleep(2.0)

    def to_utf8(self, string):
        charset = chardet.detect(string)['encoding']
        if charset is None:
            return string
        elif charset != 'utf-8' and charset == 'GB2312':
            charset = 'gb18030'
        try:
            return string.decode(charset).encode('utf-8')
        except Exception as e:
            print 'chardet error:', e

    def _request(self, url, data=None):
        for _ in range(4):
            if data is None:
                return requests.get(url, timeout=30.0).content
            else:
                return requests.post(url, data, timeout=30.0).content
        print self.__class__.__name__, 'request error!'
        return 'none'

    def recruit(self, key):
        url = 'http://opendata.baidu.com/zhaopin/s?wd=%s&rn=18&p=mini&style=list&type=' % key
        document = PyQuery(unicode(self.downloader(url), 'utf-8'))
        zp_bd = self.__info.search(document('.op_job_centerNavTip').text())
        return zp_bd.group() if zp_bd is not None else '0'

    def news(self, key):
        url = 'http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1' % urllib.quote_plus(key)
        document = PyQuery(unicode(self.downloader(url), 'utf-8'))
        print document('.nums').text()
        news_bd = self.__info.search(document('.nums').text().replace(',', ''))
        return news_bd.group() if news_bd is not None else '0'

    def patent(self, key):
        url_s = 'http://publicquery.sipo.gov.cn/txn801507.do?'\
                'select-key:startPage=%s&select-key:endPage=%s&select-key:currentPageNo=1&select-key:famingmc=&'\
                'select-key:shenqingh=&select-key:diyisqrxm=%s&select-key:fromshenqingr=&select-key:toshenqingr=&'\
                'select-key:chaxunbj=0'
        copy_url = url_s
        document = PyQuery(unicode(self.to_utf8(self._request(url_s % ('0', '5', key))), 'utf-8'))
        pages_list = re.compile('(\d+)').findall(document('.box_page').text())
        print 'sipo patent [pages_list]:', pages_list
        if not pages_list:
            return '0'
        if len(pages_list) == 1:
            return str(document('.xh').size())
        else:
            req_uel = copy_url % (str((int(pages_list[-1]) - 1) * 5), str(int(pages_list[-1]) * 5), key)
            docu = PyQuery(unicode(self.to_utf8(self._request(req_uel)), 'utf-8'))
            return str((int(pages_list[-1]) - 1) * 5 + docu('.xh').size())

    def court(self, key):
        url = 'http://www.court.gov.cn/extension/search.htm?'
        data = {'keyword': key, 'caseCode': '', 'wenshuanyou': '', 'anjianleixing': '', 'docsourcename': '',
                'court': '', 'beginDate': '2014-01-01', 'endDate': str(datetime.date.today()),
                'adv': '1', 'orderby': '', 'order': ''}
        try:
            text = self.__court.findall(self.downloader(url + urllib.urlencode(data)))[0]
            ct = self.__info.search(text)
            return ct.group() if ct is not None else '0'
        except:
            return '0'

    def aleax(self, site):
        ret = {'rank': '0', 'ip': '0', 'pv': '0'}
        if not site.strip():
            return ret
        elif 'http://' in site or 'https://' in site:
            site = site[site.find('://') + 3:]
        if site.find('/') != -1:
            site = site[:site.find('/')]

        sk = self.__grade.findall(self.downloader('http://www.alexa.cn/index.php?url=%s' % site))
        print sk
        try:
            dat = dict(zip(['url', 'sig', 'keyt'], sk[0]))
            infos = self.downloader('http://www.alexa.cn/api0523.php', urllib.urlencode(dat)).split('*')[:16]
            ranks = [v for i, v in enumerate(infos[:8]) if i % 2 == 0 and v != '-']
            ips_pvs = [(v, infos[10:][i + 1]) for i, v in enumerate(infos[10:]) if i % 2 == 0 and v != '-']
            if ranks and ranks[0]:
                ret['rank'] = ranks[0]
            if ips_pvs:
                _ip, _pv = float(ips_pvs[0][0].replace(',', '')), float(ips_pvs[0][1].replace(',', ''))
                if 0 <= _ip <= 1:
                    ret['ip'] = str(int(_ip * 3000))
                    ret['pv'] = str(int(_ip * 3000 * _pv))
                else:
                    ret['ip'] = str(int(_ip) * 3000)
                    ret['pv'] = str(int(_ip) * 3000 * int(_pv))
        except:pass
        return ret

    def main(self, ks):
        wiki = {'key': [self.recruit, self.news, self.court, self.patent], 'site': self.aleax}  # self.patent
        results = ['0'] * 4
        pool = ThreadPool(6)
        try:
            results = pool.map(lambda v: v[0](v[1]), [(f, ks[0]) for f in wiki['key']])  # [(wiki['site'], ks[1])]
            return results
        except IndexError:
            pass
        finally:
            pool.close()
            pool.join()
        return results


def job_news_court_patent(p_name, skip=2):
    pt = Partage()
    coll = db[db_name][table_name_insert]
    # for i, dc in enumerate(xlsx_infos()):
    for i, dc in enumerate(comp_infos()):
        print dc
        if i <= skip:
            continue

        if 'id' not in dc:
            log(log_normal, '%s company not id ' % dc['name'].encode('u8'), 'id:%d' % i)
            raise KeyError("`d` dictionary hasn't key `id`")

        name = dc['name'].encode('u8')
        result = pt.main((name, ))
        db_insert(coll, {'id': dc['id'], 'date': datetime.datetime.now(), 'job': result[0], 'news': result[1], 'court': result[2], 'tm': result[3], 'name': name, 'web': dc['web']})
        print p_name, '=>', 'id:', i, name, '\n', result, '\n\n'
        log(log_normal, strftime('%Y-%m-%d %H:%M:%S %A'), 'id: %d' % i, name, str(result))
        time.sleep(randint(3, 8))
    else:
        log(log_normal, 'all ok!')
    db.close()


def alexa_rank(p_name, skip=2):
    pt = Partage()
    coll = db[db_name][table_name_insert]
    # for k, d in enumerate(xlsx_infos()):
    for k, d in enumerate(comp_infos()):
        if k <= skip:
            continue

        if 'id' not in d:
            log(log_alexa, '%s company not id ' % d['name'].encode('u8'), 'id:%d' % k)
            raise KeyError("`d` dictionary hasn't key `id`")

        rets, name, web = {'rank': '0', 'ip': '0', 'pv': '0'}, d['name'].encode('u8'), d['web'].encode('u8')
        if web:
            rets = pt.aleax(web)
            t = randint(50, 70)
            print p_name, '=>', k, name, web, '\n', rets, '\nnow sleeping %d seconds!\n' % t
            log(log_alexa, strftime('%Y-%m-%d %H:%M:%S %A'), name, 'id: %d' % k, web, str(rets))
            time.sleep(t)
        db_insert(coll, {'id': d['id'], 'date': datetime.datetime.now(), 'rank': rets.get('rank'), 'ip': rets.get('ip'), 'pv': rets.get('pv')})
    else:
        log(log_alexa, 'all ok !')
    db.close()


def multi_process():
    from multiprocessing import Process
    jobs = []
    for func, p_name in [(job_news_court_patent, 'job_news'), (alexa_rank, 'alexa')]:
        p = Process(target=func, args=(p_name, ))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()


def baidu_news(key=None):
    import pymongo
    pt = Partage()
    _db = pymongo.MongoClient('192.168.0.212', 27017)
    coll = _db.crawler.comp_baidu_info

    dt = lambda v: datetime.datetime.strptime('%s %s' % tuple(v) + ':00', '%Y-%m-%d %H:%M:%S')
    url = 'http://news.baidu.com/ns?word=%s&pn=%s&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'
    for k, d in enumerate(comp_infos()):
        if k < 3513:
            continue

        count, parse_key = 0, urllib.quote_plus(d['name'].encode('u8'))
        while 1:
            document = PyQuery(unicode(pt.downloader(url % (parse_key, count * 20)), 'utf-8'))
            links, ads = document('.c-title'), document('.c-author')
            is_end = True if links.length == 0 else False
            for i in range(links.length):
                lt, author_dates = links.eq(i), ads.eq(i).text().split()
                if len(author_dates) < 3:
                    continue
                source, pdt = author_dates[0], dt(author_dates[1:])
                href, title = lt.find('a').attr('href'), lt.text().replace(' ', '')
                data = {'id': d['id'], 'name': d['name'], 'href': href, 'title': title, 'source': source, 'pdt': pdt}
                if coll.find_one({'id': d['id'], 'href': href}, {'name': 1}) is not None:
                    is_end = True
                    break
                coll.insert(data)

            if is_end is True:
                break
            print 'k:', k + 1, d['name'], 'page:%s done!' % (count + 1)
            count += 1
            time.sleep(randint(10, 20) * 0.18)
    _db.close()


if __name__ == '__main__':
    baidu_news()