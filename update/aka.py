# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient


# client = MongoClient('10.0.250.10')
# collection = client['news']['hotnews_analyse']

client = MongoClient('192.168.100.20')
collection = client['test']['test_news']

query = {'_id': ObjectId('57be2269e4b09fd213100470')}
docs = collection.find_one(query, {'sum': 1})

new_sum = '#&#该公司管理层指，截至6月底，公司拥有1420万平方米土储，主要分布于长三角及南中国海地区城市，' \
          '料足够支撑公司未来3至5年发展需求，未来将𣈴准苏南、广西、上海等地重点发展新项目，并增加住宅用地储备。' \
          '#&#绿地金服总裁杨晓冬指，绿地金服上半年实现零坏账、零违约及零延期兑付，料未来将继续朝在线财富管理、' \
          '资产管理及科技数据服务发展。'
# collection.update(query, {'$set': {'sum': new_sum, 'upt': datetime.now()}})
collection.update(query, {'$set': {'sum': codecs.encode(new_sum, 'utf-8'), 'upt': datetime.now()}})
client.close()

print ['𣈴'.encode('gb18030')]
print ['瞄']
print codecs.encode('𣈴', 'utf-8')

