# import subprocess
#
#
# child = subprocess.call('ps aux|grep run_jobs.py', shell=True)
# print child
import time
from random import randint
from clean_index import CacheTest


class Test1(object):
    def __init__(self):
        self.t = CacheTest()
        cache = self.t.__class__.cache
        print 'id 1:', id(self.t), id(cache), len(cache)

    def add(self):
        for d in range(100, 110):
            self.t.__class__.cache.add(d)
            time.sleep(randint(1, 3))
            print d, len(self.t.__class__.cache)


if __name__ == '__main__':
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.executors.pool import ThreadPoolExecutor

    jobstores = {
        'default': MemoryJobStore()
    }

    # using ThreadPoolExecutor as default other than ProcessPoolExecutor(not work) to executors
    executors = {
        'default': ThreadPoolExecutor(4),
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    app = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    def task():
        print len(CacheTest.cache)

    app.add_job(task, 'interval', seconds=2)
    app.start()
