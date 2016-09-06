from tasks import add

add.delay(4, 4)


if __name__ == "__main__":
    import amqp
    from celery.app.amqp import AMQP
    from celery.app.task import Task
    from collections import defaultdict, deque
    # conn = amqp.Connection()
    # chan = conn.channel()
    d = deque()

    if deque():
        print 1000

