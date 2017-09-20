from math import copysign
from django.conf import settings

import logging
import os
import sys
import django


logger = logging.getLogger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if not settings.configured:
    """setting the Django env()"""
    logger.debug('settings.configured: {0}'.format(settings.configured))
    sys.path.append(BASE)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enterprise.settings.local')
    django.setup()
    logger.debug('settings.configured: {0}'.format(settings.configured))
    from django_q.tasks import async, result, Async


def test_async_a():
    # create the task
    async('math.copysign', 2, -2)

    # or with import and storing the id
    task_id = async(copysign, 2, -2)

    # get the result
    task_result = result(task_id)

    # result returns None if the task has not been executed yet
    # you can wait for it
    task_result = result(task_id, 200)

    # but in most cases you will want to use a hook:
    async('math.modf', 2.5, hook='radars.hooks.print_result')


def test_async_b():
    # instantiate an async task
    a = Async('math.floor', 1.5, group='math')

    # you can set or change keywords afterwards
    a.cached = True

    # run it
    a.run()

    # wait indefinitely for the result and print it
    #print(a.result(wait=-1))

    # change the args
    a.args = (2.5,)

    # run it again
    a.run()

    # wait max 10 seconds for the result and print it
    print(a.result(wait=10))


def test_q_option():
    opts = {'hook': 'radars.hooks.print_result', 'group': 'fruit', 'timeout':1800}
    async('radars.tasks.order_fruit', fruit='APPLE', num_fruit=1, q_options=opts)


def test_chains():
    pass


if __name__ == '__main__':
    
