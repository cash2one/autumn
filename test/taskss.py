import time
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('_tasks', backend='amqp://')

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    # time.sleep(5)
    return x + y


@app.task(bind=True)
def error_handler(self, uuid):
    logger.info('uuid: %s' % uuid)
    result = self.app.AsyncResult(uuid)
    logger.info('Task {0} raised exception: {1!r}\n{2!r}'.format(
          uuid, result.result, result.traceback))

if __name__ == '__main__':
    # print 'name:', add.name
    print app.tasks
