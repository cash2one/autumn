# -*- coding: utf-8 -*-

from multiprocessing import Process
from crawler.cloud_360.db_handler import data_gather_copy
from crawler.cloud_360.sina_weibo import weibo
from crawler.cloud_360.partage import job_news_court_patent, alexa_rank


def crawler_cloud():
    multi_jobs = []
    func_args = [('job_news', job_news_court_patent, -1), ('alexa_rank', alexa_rank, -1), ('weibo', weibo, -1), ]
    for name, func, skip in func_args:
        p = Process(target=func, args=(name, skip))
        multi_jobs.append(p)
        p.start()

    for job in multi_jobs:
        job.join()

    print 'copy data from `ee_comp_data` to `ee_comp_gather_copy` now...'
    data_gather_copy()
    print 'copy over, ok!'


if __name__ == '__main__':
    crawler_cloud()
