# encoding=utf-8
from __future__ import unicode_literals
import re

import requests


def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/44.0.2403.157 Safari/537.36',
    }

    for _ in range(3):
        try:
            r = requests.get(url, headers=header, timeout=20)
            return r.content
        except:
            pass
    return ''


def extract():
    url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=南京'
    title_href_rule = re.compile(r'<h3 class="c-title"><a href="(.*?)".*?>(.*?)</a></h3>', re.S)
    raw_html = get_html(url)

    total_findall = title_href_rule.findall(raw_html)

    for url, title in total_findall:
        print url, title


if __name__ == '__main__':
    extract()

