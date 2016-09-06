#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import rsa
import json
import time
import urllib
import urllib2
import cookielib
import base64
import binascii
import chardet
from time import strftime
from datetime import datetime
from string import letters, digits
from random import choice, randint, sample
from multiprocessing.dummy import Pool as ThreadPool
from crawler.cloud_360.config import db, db_name, table_name_insert
from crawler.cloud_360.config import account, password, cookie_file, log_weibo
from crawler.cloud_360.db_handler import log, data_gather_copy, db_insert, comp_infos


class SinaWeibo(object):
    """
        目前这是个半成品，因为需要验证码情况下，此方法行不通，如何突破验证码的问题待以后解决。
        Add: （1）、登陆问题， 可能一次就登陆成功，可能遇到验证码的问题（登陆验证码无法解决， 目前也不可能解决）；
             （2）、登陆成功后，机器连续的抓取数据只能10条或20几条数据，后面便会出现验证码已验证是不是机器所为；
             （3）、目前采用的是时间间隔拉距的办法，即通过一定的时间间隔，避免机器式狂抓而出现验证码问题。此法虽然
                    是一个解决抓取的途径，但在速度上比较慢，不适宜快速抓取。
        `reference`: https://github.com/yoyzhou/weibo_login/blob/master/weibo_login.py
    """
    def __init__(self, user_name, password, cookies_file=None):
        self.__user_name = user_name
        self.__password = password
        self.__cookie_file = cookies_file
        self.__cookie_jar = None

    def download(self, url, data=None, headers=None):
        data = urllib.urlencode(data) if data is not None else data
        headers = {} if headers is None else headers
        for _ in range(3):
            req = urllib2.Request(url) if not data else urllib2.Request(url, data, headers)
            try:
                response = urllib2.urlopen(req, timeout=30.0)
                html = response.read()
                response.close()
                return html
            except Exception as e:
                print 'open web error:', e, self.__class__.__name__
        return ''

    def reason(self, url):
        parse = url.replace('"', '')
        params = dict([tuple(v.split('=')) for v in parse[parse.find('?') + 1:].split('&')])
        why = urllib.unquote_plus(params.get('reason', 'None'))
        charset = chardet.detect(why)['encoding']
        return '原因不详' if chardet is None else why.decode(charset).encode('u8')

    def server_time(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' \
            'su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)' % self.get_su()
        s_json = self.download(url).replace('.', '')
        try:
            data = json.loads(s_json[s_json.find('(') + 1:-1])
            server_time = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return server_time, nonce, pubkey, rsakv
        except (IndexError, KeyError) as e:
            print 'get server time error:[', e, ']!'
            return None

    def get_su(self):
        return base64.encodestring(urllib.quote(self.__user_name)).strip()

    def get_sp(self, server_time, nonce, pubkey):
        key = rsa.PublicKey(int(pubkey, 16), 65537)
        sp = binascii.b2a_hex(rsa.encrypt(server_time + '\t' + str(nonce) + '\n' + self.__password, key))
        return sp

    def post_data(self):
        st, nce, pky, kv = self.server_time()
        sp = self.get_sp(st, nce, pky)
        post = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': '',
            'vsnf': '1',
            'su': self.get_su(),
            'service': 'miniblog',
            'servertime': st,
            'nonce': nce,
            'pwencode': 'rsa2',
            'rsakv': kv,
            'sp': sp,
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        return post

    def generate_cookie(self):
        self.__cookie_jar = cookielib.LWPCookieJar()
        cookie_support2 = urllib2.HTTPCookieProcessor(self.__cookie_jar)
        opener2 = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
        urllib2.install_opener(opener2)

    def handler_cookie(self):
        if os.path.exists(self.__cookie_file):
            try:
                cookie_jar = cookielib.LWPCookieJar(self.__cookie_file)
                cookie_jar.load(ignore_discard=True, ignore_expires=True)
            except cookielib.LoadError:
                print 'loading cookie error!'
                self.generate_cookie()
            else:
                cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
                opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                print 'Loading cookies success.'
        else:
            self.generate_cookie()

    def login(self):
        self.handler_cookie()

        feed_back = self.download(
            url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',
            data=self.post_data(),
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0'})

        ### if match, login is success.
        regex_url = re.compile(r"location\.replace\(\'(.*?)\'\)", re.S).search(feed_back)
        if regex_url is None:
            regex_error = re.compile(r"location\.replace\((.*?)\)", re.S).search(feed_back).group(1)
            print 'login error, [reason]:', self.reason(regex_error)
        else:
            self.download(regex_url.group(1))
            if self.__cookie_jar:
                self.__cookie_jar.save(self.__cookie_file, ignore_discard=True, ignore_expires=True)
            print 'login success!'
            return 1
        return 0


class WeiboCrawler(SinaWeibo):
    def __init__(self, user_name, password, cookies_file):
        super(WeiboCrawler, self).__init__(user_name, password, cookies_file)
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0', 'Referer': ''}
        self.__fans_wbs = re.compile(r'class=\\"star_num\\">(.*?)<\\/p>')
        self.__fwb = re.compile(r'<a.*?>(.*?)<\\/a>')
        self.__t_block = re.compile(r'<div class=\\\"search_num\\\"><span>(.*?)<\\/span>', re.S)
        self.__talk = re.compile(r'\d+')
        self._talk_no = re.compile(r'<div class=\\"pl_noresult\\">', re.S)
        self._talk_ot = re.compile(r'<div class=\\\"WB_feed_detail clearfix\\\">', re.S)

    def fans_wb(self, key):
        ### return is fans and weibo num
        time.sleep(randint(3, 10))
        rt = letters + digits
        refer = 'http://s.weibo.com/weibo/%s&' % key + \
                urllib.urlencode(dict([(choice(rt), sample(rt, randint(1, 5))) for _ in range(randint(0, 4))]))
        self.__headers['Referer'] = refer
        fan_wb = self.__fans_wbs.search(self.download(refer, headers=self.__headers))
        if fan_wb:
            fw = self.__fwb.findall(fan_wb.group(1))[1:]
            if json.dumps(u'万').strip('"') in fw[0]:
                return str(int(re.compile(r'\d+').findall(fw[0].decode('unicode-escape'))[0]) * 10000), fw[1]
            return fw
        return '0', '0'

    def talk(self, key):
        rt = letters + digits
        refer = 'http://s.weibo.com/weibo/%s&nodup=1&' % key + \
                urllib.urlencode(dict([(choice(rt), sample(rt, randint(1, 5))) for _ in range(randint(0, 4))]))
        self.__headers['Referer'] = refer
        html = self.download(refer, headers=self.__headers)
        t_alk = self.__t_block.search(html)
        if t_alk:
            return self.__talk.search(t_alk.group(1).decode('unicode-escape')).group()
        return '0' if self._talk_no.search(html) else str(len(self._talk_ot.findall(html)))

    def main(self, key):
        rets = [('0', '0'), '0']
        pool = ThreadPool(2)
        try:
            rets = pool.map(lambda f: f[0](f[1]), [(fu, '%%22%s%%22' % key) for fu in [self.fans_wb, self.talk]])
        except IndexError:
            pass
        finally:
            pool.close()
            pool.join()
        return rets


def weibo(p_name, skip=-1):
    wb = WeiboCrawler(account, password, cookie_file)
    if wb.login():
        coll = db[db_name][table_name_insert]
        # for k, d in enumerate(xlsx_infos()):
        for k, d in enumerate(comp_infos()):
            if k <= skip:
                continue

            if 'id' not in d:
                log(log_weibo, '%s company not id ' % d['name'].encode('u8'))
                raise KeyError("`d` dictionary hasn't key `id`")
            if k % 200 == 0:
                wb.login()

            ret = wb.main(d['name'].encode('u8'))
            db_insert(coll, {'date': datetime.now(), 'weibo': ret[0][1], 'fans': ret[0][0], 'talk': ret[1], 'id': d['id']})
            t = randint(40, 60)
            print p_name, '=>', k + 1, d['name'], '\n', ret, '\nnow sleeping %d seconds!\n' % t
            time.sleep(t)
            log(log_weibo, strftime('%Y-%m-%d %H:%M:%S %A'), 'id: %d' % k, d['name'].encode('u8'), str(ret),
                'sleeping %d seconds!' % t)
        else:
            log(log_weibo, 'all ok')
    else:
        log(log_weibo, 'login error!')
    data_gather_copy()
    db.close()


def test(key):
    sur = 'shukuyun@163.com'
    pwd = 'shukuYUN!'
    wb = WeiboCrawler(sur, pwd, cookie_file)
    if wb.login():
        print key
        print wb.main(key), '\n'


if __name__ == '__main__':
    kts = '环球市场集团'
    weibo()





