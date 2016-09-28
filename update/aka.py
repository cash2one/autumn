# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient


client = MongoClient('10.0.250.10')
collection = client['news']['hotnews_analyse']

# client = MongoClient('192.168.100.20')
# collection = client['test']['test_news']

# query = {'_id': ObjectId('57d74d4ee4b0a3b2adb3dfce')}
# docs = collection.find_one(query, {'sum': 1})
#
# new_sum = '#&#港股嘛，昨与美股同是天涯沦落人，就是质到落全日最低位收市，升跌比例重现一九之比，' \
#           '这等市况唔好谂几时捞货住，系要谂几时反弹可以走埋手上的货先。#&#和美医疗（1509）中期业绩平平，' \
#           '收入倒退3.4%，毛利率下跌2.6个百分点，其他收入带动下纯利微增5%，绩后随即出现大成交下跌，但很快即获承接，' \
#           '重回业绩公布前的水平，值得留意是业绩前，公司不停进行回购，回购价曾见6蚊，故可趁近日市况回调下𥄫实。'
# collection.update(query, {'$set': {'sum': new_sum, 'upt': datetime.now()}})
# client.close()

query = {
    'uid': 'f47bbfe862764959e779e8cf67d303c8'
}

for doc in collection.find(query):
    _id = doc['_id']
    collection.remove({'_id': _id})

client.close()




