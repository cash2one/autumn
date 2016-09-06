# coding=utf-8
from __future__ import unicode_literals
import hashlib
import re

from pymongo import MongoClient


def populate_md5(value):
    if not isinstance(value, basestring):
        raise ValueError('md5 must string!')
    m = hashlib.md5()
    try:
        m.update(value)
    except UnicodeEncodeError:
        m.update(value.encode('u8'))
    return m.hexdigest()


def recognise_chz(string):
    chz_chars = []
    chz_regex = re.compile(r'[\u4e00-\u9fbf]', re.S)
    letters_regex = re.compile(r'[0-9A-Za-z]', re.S)

    for char in string:
        if chz_regex.search(char) or letters_regex.search(char):
            chz_chars.append(char)
    return ''.join(chz_chars)


def get_md5():
    client = MongoClient("192.168.250.208", 27017)
    db = client["news"]
    collection = db["hotnews_analyse"]
    date = {
        "$gte": "20150321235959"
    }
    ret = []
    data = collection.find(
        {
            "dt": {
                "$lte": "20150321235959"
            }
        },
        {"url": 1, "t": 1}
    )
    for detail in data:
        url_md5 = populate_md5(detail["url"])
        tit_md5 = populate_md5(recognise_chz(detail["t"]))
        ret.append(url_md5)
        ret.append(tit_md5)
    return ret


if __name__ == '__main__':
    data = get_md5()
    print len(data)
