# encoding:utf8
from collections import defaultdict
import pymongo

client_20 = pymongo.MongoClient('192.168.100.20')


def copy_table():
    # coll = client_20.ada.constituent
    # coll = client_20.ada.index_members
    coll = client_20.ada.index_members_copy

    for docs in coll.find():
        s_code = docs['s_code']

        if len(s_code) != 6:
            new_s_code = '0' * (6 - len(s_code)) + s_code
            if '!' in s_code:
                coll.update({'_id': docs['_id']}, {'$set': {'s_code': s_code[:-2]}})
            print 'err:', docs['_id'], s_code, docs['cat'], new_s_code


def clean_index_one():
    # 从 192.168.100.20d ada.constituent 将数据清晰到ada.index_members中
    coll_ada = client_20.ada.constituent
    coll_index = client_20.ada.index_members

    for ind, docs in enumerate(coll_ada.find(), 1):
        key = docs['p_code'] + docs['s_code']
        query = {'p_code': docs['p_code'], 's_code': docs['s_code']}

        members = coll_index.find(query)

        if not members.count():
            docs.pop('_id')
            # coll_index.insert(docs)
        else:
            members_sorted = sorted(members, key=lambda item: item['in_dt'], reverse=True)
            required_docs = members_sorted[0]

            if required_docs['in_dt'] <= docs['in_dt']:
                if not required_docs['out_dt']:
                    pass
                else:
                    docs.pop('_id')
                    # coll_index.insert(docs)
            else:
                if not required_docs['out_dt']:
                    # coll_index.update({'_id': required_docs['_id']}, {'$set': {'in_dt': docs['in_dt']}})
                    pass
                print 'NO normal:', required_docs['_id'], docs['_id']

        # print 'index: [{}]'.format(ind)

    client_20.close()


def clean_index_two():
    # 从 192.168.100.20d ada.index_members 将数据清晰到 ada.constituent中
    rt_data = defaultdict(list)
    constituent_data = defaultdict(list)

    coll_members = client_20.ada.index_members_copy
    coll_const = client_20.ada.constituent
    coll_index = client_20.ada.index_members

    for r_docs in coll_members.find():
        r_key = r_docs['p_code'] + r_docs['s_code']
        rt_data[r_key].append(r_docs)

    for c_docs in coll_members.find():
        c_key = c_docs['p_code'] + c_docs['s_code']
        constituent_data[c_key].append(c_docs)

    for ind, items in enumerate(rt_data.iteritems(), 1):
        m_key, values = items
        values.sort(key=lambda it: it['in_dt'], reverse=True)

        if len(values) >= 2:
            print values
            break

        need_docs = values[0]

        if need_docs['out_dt']:
            pass
        else:
            mod_values = constituent_data.get(m_key)

            if mod_values:
                mod_docs = sorted(mod_values, key=lambda t: t['in_dt'], reverse=True)[0]


def compare():
    coll_const = client_20.ada.constituent
    coll_index = client_20.ada.index_members

    mem_set = {d['p_code'] + d['s_code'] for d in coll_index.find()}
    const_set = {d['p_code'] + d['s_code'] for d in coll_const.find()}

    print len(mem_set - const_set)
    print len(const_set - mem_set)


if __name__ == '__main__':
    # clean_index_one()
    # clean_index_two()
    compare()
