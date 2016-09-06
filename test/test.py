from celery.utils.log import get_task_logger
from celery.local import PromiseProxy

from celery.exceptions import Ignore
from celery import states
from celery.app.control import Control

# from celery.signals import