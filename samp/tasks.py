from __future__ import absolute_import

from samp._celery import app


@app.task
def add(x, y):
    _sum = x + y
    return _sum


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(members):
    return sum(members)
