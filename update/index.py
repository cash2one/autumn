import re
import pymongo

client_95 = pymongo.MongoClient('122.144.134.95')
client_20 = pymongo.MongoClient('192.168.100.20')
coll_95 = client_95.ada.index_members_a
coll_20 = client_20.ada.index_members_a
coll_20_copy = client_20.ada.index_members_a_copy_20160622

# coll_20_copy.insert_many(coll_20.find())

coll_95.insert_many(coll_20.find())
# cond = {'cat': re.compile(r'sse|szse|cnindex')}
# keys_filter = [d['p_code'] + d['s_code'] for d in coll_20.find(cond)]
# print len(keys_filter), len(set(keys_filter))
#
# query = {'cat': 'csindex'}
# for docs in coll_20.find(query):
#     key = docs['p_code'] + docs['s_code']
#
#     if key in keys_filter:
#         print coll_20.remove({'_id': docs['_id']})

client_95.close()
client_20.close()
