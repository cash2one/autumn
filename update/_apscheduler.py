import time
import os
import thread
import threading
from redis import Redis
from datetime import datetime

from os.path import dirname, abspath

from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor

HOST = '192.168.0.223'
PORT = 27017
# client = MongoClient(HOST, PORT)


def create_sqlite():
    sqlite_path = dirname(abspath(__file__))
    for sql_path in os.listdir(sqlite_path):
        if sql_path.endswith('.db'):
            os.remove(os.path.join(sqlite_path, sql_path))

create_sqlite()

jobstores = {
    # 'mongo': MongoDBJobStore(database='test', collection='job', client=client),
    # 'default': MemoryJobStore()
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
}

executors = {
    'default': ThreadPoolExecutor(4),
    # 'processpool': ProcessPoolExecutor(3)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)


def my_job1(schedule):
    print 'stt:', datetime.now()
    print 'jobs:', schedule.get_jobs()
    time.sleep(10)
    print 'end:', datetime.now()


def sub():
    print 'redis Sub start...'
    print 'sub:', sub
    redis_client = Redis()
    print 'id:', id(redis_client)
    sb = redis_client.pubsub()
    sb.subscribe('test_aps')

    for msg in sb.listen():
        print 'msg:', msg


# @scheduler.scheduled_job('interval', seconds=5)
def my_job3():
    print 'jon 3 run', datetime.now()
    time.sleep(60 * 3)


# @scheduler.scheduled_job('interval', seconds=3)
# @scheduler.scheduled_job('cron', second='7', hour='15,16')
# @scheduler.scheduled_job(trigger='interval', minutes=1, seconds=30,)
def my_job4():
    print 'job4 run:', datetime.now()


print 'Now      :', datetime.now()
beat = {'trigger': 'cron', 'minute': '*/41', 'hour': '15'}

scheduler.add_job(my_job3, trigger='cron', hour='13-23', second='*/20')
scheduler.add_job(my_job4, trigger='cron', hour='13-23', second='*/20')
try:
    scheduler.start()
except SystemExit:
    print '0000'
    # client.close()

