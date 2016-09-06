import re
from collections import defaultdict
from pymongo import MongoClient

client_95 = MongoClient('122.144.134.95')
client_20 = MongoClient('192.168.100.20')

# coll_95 = client_95.ada.index_members_a
coll_20_index = client_20.ada.index_members_a
coll_20 = client_20.ada.wind

# #### copy 95 index_members_a data to 20 index_members_a ####
# coll_20_index = client_20.ada.index_members_a
# for docs in coll_20_index.find({"sign": "1"}):
#     _id = docs['_id']
#     coll_20_index.update({'_id': _id}, {"$set": {'sign': '0', 'out_dt': '20160620'}})
# # coll_20_index.insert_many(coll_95.find())
# #### copy 95 index_members_a data to 20 index_members_a ####

count = 0
data_20 = defaultdict(list)
keys_20_web = {d['p_code'] + d['s_code']: d for d in coll_20_index.find()}
print len(keys_20_web)

for docs in coll_20.find():
    key = docs['p_code'] + docs['s_code']
    data_20[key].append(docs)

for _key, values in data_20.iteritems():
    values.sort(key=lambda d: d['in_dt'], reverse=True)

for t_key, t_values in data_20.iteritems():
    is_continue = False
    for m_docs in t_values:
        count += 1
        _id = m_docs.pop('_id')
        p_code, s_code = m_docs['p_code'], m_docs['s_code']
        m_key = p_code + s_code

        if m_key not in keys_20_web:
            coll_20_index.insert_one(m_docs)
            pass
        else:
            in_dt = m_docs['in_dt']
            out_dt = m_docs['out_dt']

            if not is_continue:
                is_continue = True
                cond = {'_id': keys_20_web[m_key]['_id']}

                if not out_dt:
                    coll_20_index.update(cond, {'$set': {'in_dt': in_dt, 'out_dt': out_dt}})
                else:
                    coll_20_index.update(cond, {'$set': {'in_dt': in_dt, 'out_dt': out_dt, 'sign': '1'}})
            else:
                coll_20_index.insert_one(m_docs)
                pass
        print 'Count <%s>, {"p_code": "%s", "s_code": "%s"}, Done!' % (count, p_code, s_code)

client_95.close()
client_20.close()
