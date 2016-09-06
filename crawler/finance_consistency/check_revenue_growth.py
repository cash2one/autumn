# -*- coding: UTF-8 -*-
from __future__ import print_function

import config_params
import request_api
import query_set
from multiprocessing.dummy import Pool as ThreadPool


def check_revenue_growth():
    coll_ltm = getattr(config_params, 'coll_{0}_ltm'.format('tpl'), None)
    assert coll_ltm is not None, "tpl don't need what logical get"

    arguments = []
    queryset_dict = query_set.get_data_revenue_growth()
    api_args = ['rpt', 'secu', 'y', 'fp', 'q', '_id', 'ctyp']

    for dct in queryset_dict:
        query_string = '#'.join([str(dct[k]) for k in api_args])
        item = ('only_ltm', (query_string, dct['_id']))
        arguments.append(item)

    pool = ThreadPool(14)
    ids_set = pool.map(request_api.request_interface, arguments)
    pool.close()
    pool.join()

    for ids in [_id for _id in ids_set if _id]:
        coll_ltm.update({'_id': ids}, {'$set': {'stat': 2}})


if __name__ == '__main__':
    check_revenue_growth()
