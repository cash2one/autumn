import os
from datetime import datetime
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor


jobstores = {
    'default': MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(1),
    # 'processpool': ProcessPoolExecutor(10)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
# app = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
# app = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
# pid = os.getpid()


# @app.scheduled_job(trigger='interval', seconds=5, misfire_grace_time=10)
# def job():
#     with open('log.txt', 'a') as fp:
#         fp.write('[{}]: pid <{}>, out pid <{}>\n'.format(datetime.now(), os.getpid(), pid))
#
# app.start()


def job1():
    print 'job1:', datetime.now()


def job2():
    print 'job2:', datetime.now()


def job3():
    print 'job3:', datetime.now()


def job4():
    print 'job4:', datetime.now()


app = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
app.add_job(job1, trigger='interval', seconds=5)
app.add_job(job2, trigger='interval', seconds=5)
app.add_job(job3, trigger='interval', seconds=5)
app.add_job(job4, trigger='interval', seconds=5)
app.start()
