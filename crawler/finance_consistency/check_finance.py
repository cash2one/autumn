# -*- coding: UTF-8 -*-
from __future__ import print_function

import time
import query_set
import config_params
import request_api
from multiprocessing.dummy import Pool as ThreadPool


def check_finance_consistency(typ):
    coll_ltm = getattr(config_params, 'coll_{0}_ltm'.format(typ), None)
    coll_ytd = getattr(config_params, 'coll_{0}_ytd'.format(typ), None)
    assert coll_ltm is not None and coll_ytd is not None, 'typ value is not excepted.'

    typ_ltm_dict, typ_ytd_dict = query_set.query_set_from_table(typ)

    ltm_set = {sk for sk in typ_ltm_dict}
    ytd_set = {sk for sk in typ_ytd_dict}
    ltm_not_in_ytd = [each_ltm for each_ltm in ltm_set if each_ltm not in ytd_set]
    ytd_not_in_ltm = [each_ytd for each_ytd in ytd_set if each_ytd not in ltm_set]
    count_ltm, count_ytd = len(ltm_not_in_ytd), len(ytd_not_in_ltm)
    count_ltm, count_ytd = len(ltm_not_in_ytd), len(ytd_not_in_ltm)

    # ('rpt', 'secu', 'y', 'fp', 'q', 'stdtyp', 'ctyp') is identical with need_fields of quert_set
    print('Not In:count ltm:{0}, count ytd: {1}'.format(count_ltm, count_ytd))
    query_ltm_all = [(typ + '_ltm_not_in_ytd', (each, typ_ltm_dict[each]['_id'])) for each in ltm_not_in_ytd]
    query_ytd_all = [(typ + '_ytd_not_in_ltm', (item, typ_ytd_dict[item]['_id'])) for item in ytd_not_in_ltm]

    pool = ThreadPool(8)
    # request_ltm_ids = pool.map(request_interface, query_ltm_all)
    request_ytd_ids = pool.map(request_api.request_interface, query_ytd_all)
    pool.close()
    pool.join()

    # print('Now will update [{0}] `stat` value'.format(coll_ltm.full_name))
    # for ltm_id in [id_l for id_l in request_ltm_ids if id_l]:
    #     coll_ltm.update({'_id': ltm_id}, {'$set': {'stat': 2}})

    print('Now will update [{0}] `stat` value'.format(coll_ytd.full_name))
    for ytd_id in [id_y for id_y in request_ytd_ids if id_y]:
        coll_ytd.update({'_id': ytd_id}, {'$set': {'stat': 2}})


if __name__ == '__main__':
    while 1:
        if time.strftime('%H%M') in ['1900']:
            start = time.time()
            check_finance_consistency('tpl')
            end = time.time()

            check_finance_consistency('asrep')
            end2 = time.time()
            print('tpl need time: {0}'.format(end - start))
            print('asrep need time: {0}'.format(end2 - end))
            time.sleep(20)

        if int(time.strftime('%H%M')) % 3 == 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S %A'))
            time.sleep(20)
