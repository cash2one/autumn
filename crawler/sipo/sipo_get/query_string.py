# -*- coding: UTF-8 -*-

# suit to single type `fmgb`, `fmsq`, `syxx`, `wgsq`

num_fmgb = 168341
num_syxx = 148423
query_start_date = '2010.01.01'
query_end_date = '2015.06.30'


def get_url_with_query_string(typ):
    assert typ != 'fmgb' or typ != 'syxx', ' typ must is `fmgb` or `syxx`'

    typ = typ if typ == 'fmgb' else 'xxsq'
    num_typ = {'fmgb': (num_fmgb, ''), 'xxsq': ('', num_syxx)}
    request_url = 'http://epub.sipo.gov.cn/patentoutline.action?'

    query_string = 'showType=1&' \
                   'strWord=%E5%85%AC%E5%BC%80%EF%BC%88%E5%85%AC%E5%91%8A%EF%BC%89%E6%97%A5%3DBETWEEN%5B%27{0}%27%2C%27{1}%27%5D+and+%E5%9C%B0%E5%9D%80%3D%27%E4%B8%8A%E6%B5%B7%E5%B8%82%27&' \
                   'numSortMethod=0&' \
                   'strLicenseCode=&' \
                   'selected={2}&' \
                   'numFMGB={3}&' \
                   'numFMSQ=&' \
                   'numSYXX={4}&' \
                   'numWGSQ=&' \
                   'pageSize=10&' \
                   'pageNow={page}'.format(query_start_date, query_end_date, typ, *num_typ.get(typ), page='{page}')
    return request_url + query_string


if __name__ == '__main__':
    from multiprocessing.dummy import Pool as ThreadPool

    pool = ThreadPool()
    rets = pool.map(get_url_with_query_string, ['fmgb', 'syxx'])
    pool.close()
    pool.join()

    print '\n'.join(rets)

