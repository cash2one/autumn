import time
from random import randint
from datetime import datetime
from pymongo import MongoClient
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

client = MongoClient('192.168.0.223', 27017)

jobstores = {
    'mongo': MongoDBJobStore(database='test', collection='job', client=client)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}


def job():
    _random = randint(60, 60 * 4)
    print 'sat:', datetime.now()
    print '100000->:', _random
    time.sleep(_random)
    print 'end:', datetime.now()

scheduler = BlockingScheduler(jobstores=jobstores, job_defaults=job_defaults)
store = MongoDBJobStore(database='test', collection='job', client=client)
# scheduler.add_jobstore(store, 'mongo')
scheduler.add_job(job, 'interval', minutes=2)
scheduler.start()
