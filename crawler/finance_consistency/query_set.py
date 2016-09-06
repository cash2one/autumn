# -*- coding: UTF-8 -*-

import time
import config_params


def query_set_from_table(typ):
    """ typ value must 'tpl' or 'asrep' """

    # for keys: need `rpt`, `secu`, `y`, `q`, `fp`, `stdtyp` and assure whether `ctyp` is equivalent on both sides.
    # for query data: `active` is True
    # to two records: must make keys and data of both sides is identical.
    # `rpt` of `tpl` table record is 2.1.2 or 2.3.2, `rpt` of related `asrep` is 2.1.1 or 2.3.1
    coll_ltm = getattr(config_params, 'coll_{0}_ltm'.format(typ), None)
    coll_ytd = getattr(config_params, 'coll_{0}_ytd'.format(typ), None)
    assert coll_ltm is not None and coll_ytd is not None, 'typ value is not excepted.'

    typ_ltm_dict, typ_ytd_dict = {}, {}
    rpt_values_list = ['2.1.2', '2.3.2'] if typ == 'tpl' else ['2.1.1', '2.3.1']
    needs_fields = ['rpt', 'secu', 'y', 'fp', 'q', 'stdtyp', 'ctyp']
    query_conditions = {'rpt': {'$in': rpt_values_list}, 'active': True}
    query_fields = {k: 1 for k in needs_fields}

    start_ltm = time.time()
    for k_ltm, item_ltm in enumerate(coll_ltm.find(query_conditions, query_fields).sort([('_id', 1)])):
        key_ltm = '#'.join([str(item_ltm[key]) for key in needs_fields])
        typ_ltm_dict[key_ltm] = item_ltm
    print '{0} count: {1}, need time: {2}s'.format(coll_ltm.full_name, k_ltm + 1, time.time() - start_ltm)

    start_ytd = time.time()
    for k_ytd, item_ytd in enumerate(coll_ytd.find(query_conditions, query_fields).sort([('_id', 1)])):
        key_ytd = '#'.join([str(item_ytd[key]) for key in needs_fields])
        typ_ytd_dict[key_ytd] = item_ytd
    print '{0} count: {1}, need time: {2}s'.format(coll_ytd.full_name, k_ytd + 1, time.time() - start_ytd)

    print 'typ_ltm_all count: {0}'.format(len(typ_ltm_dict))
    print 'typ_ytd_all count: {0}\n'.format(len(typ_ytd_dict))

    return typ_ltm_dict, typ_ytd_dict


def get_data_revenue_growth(typ='tpl'):
    coll_ltm = getattr(config_params, 'coll_{0}_ltm'.format(typ), None)
    assert coll_ltm is not None, "tpl don't need what logical get"
    print coll_ltm.full_name

    queryset_ltm = []
    query_conditions = {"rpt": "2.1.2", "active": True}
    query_fields = ['secu', 'y', 'ctyp', 'fp', 'rpt', 'q', '_id']
    count = coll_ltm.find(query_conditions).count()

    for k, ltm_dict in enumerate(coll_ltm.find(query_conditions).sort([('_id', 1)])):
        items = ltm_dict.get('items', []) or []
        cds = {item['cd'] for item in items}
        if 'is_tpl_1'in cds and 'is_fa_1' not in cds:
            queryset_ltm.append({ky: ltm_dict[ky] for ky in query_fields})
            # print {ky: ltm_dict[ky] for ky in query_fields}
            # break
        print 'k:{0}, progress: [{1}%]'.format(k + 1, (k + 1) / float(count) * 100)
    return queryset_ltm


if __name__ == '__main__':
    # typ_ltm_all, typ_ytd_all = query_set_from_table('sarep')

    import os
    from eggs.utils.xlsx_writer import XlsxWriter
    st = time.time()
    set_ltm = get_data_revenue_growth()
    print 'need time:', time.time() - st
    print 'set ltm count:', len(set_ltm)

    path = os.path.dirname(__file__) + '/log/'
    headers = ['_id', 'secu', 'y', 'ctyp', 'fp', 'rpt', 'q']
    open_book = XlsxWriter(path + 'rg.xlsx', headers=headers)
    for dct in set_ltm:
        open_book.write([dct[key] for key in headers])
    open_book.close()
