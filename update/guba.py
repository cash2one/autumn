# -*- coding: utf-8 -*-
import requests
from pymongo import MongoClient

db = MongoClient('192.168.100.20', 27017)
coll = db['py_crawl']['guba']


def mood_api(t):
    """
    0：中性概率     1：  正面概率    2： 负面概率
    :param t:
    :return:
    """
    url = 'http://54.223.46.84:8005/api/svm_news'
    t = {'t': t}
    print requests.post(url, data=t).content


def cal_count():
    query = {'code': '002471.sz'}
    print coll.find(query, {'_id': 1}).count()
    db.close()


if __name__ == '__main__':
    cal_count()

    mood_api('第一创业')

