#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from crawler.cloud_360.config import db, db_name, table_name_source, table_name_insert, table_gather_copy


def db_insert(coll, data):
    if coll.find_one({'id': data['id']}) is None:
        coll.insert(data)
    else:
        coll.update({'id': data['id']}, {'$set': data})


def comp_infos():
    need = {'base.name': 1, 'base.web': 1}
    coll_get = db[db_name][table_name_source]
    all_infos = []
    for d in coll_get.find({'base.typ': '0'}, need).sort([('_id', -1)]):
        if not d['base'].get('name'):
            continue

        if not d['base'].get('web'):
            d['base']['web'] = ''
        all_infos.append({'id': d['_id'], 'name': d['base']['name'], 'web': d['base']['web']})
    db.close()
    return iter(all_infos)


def xlsx_infos():
    import os
    from eggs.utils.xlsx import XlsxReader
    open_book = XlsxReader(os.path.dirname(__file__) + '/cloud_360.xlsx')
    for d in open_book.collection(**{'id': str}):
        yield d


def log(path, *args):
    _path, log_name = os.path.dirname(path), os.path.basename(path)
    if not os.path.exists(_path):
        os.makedirs(_path)

    os.chdir(_path)
    with open(log_name, 'a') as fd:
        fd.writelines('\n'.join(args) + '\n\n')


def data_gather_copy():
    from_coll = db[db_name][table_name_insert]
    copy_coll = db[db_name][table_gather_copy]
    for doc in from_coll.find().sort([('_id', -1)]):
        doc.pop('_id', None)
        if not copy_coll.find_one(doc):
            copy_coll.insert(doc)
    db.close()


