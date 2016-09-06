from __future__ import absolute_import

from celery import Celery


app = Celery('samp',
             broker='amqp://guest@localhost//',
             backend='amqp://',
             include=['samp.tasks']
             )

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)


if __name__ == '__main__':
    app.start()

