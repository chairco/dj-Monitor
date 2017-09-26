import os
import subprocess as sp
import time

from collections import OrderedDict
from contextlib import contextmanager

from django_q.tasks import async, result, async_chain, result_group
from django.conf import settings


RScript = settings.R_BIN


@contextmanager
def cd(newdir):
    """
    Context manager for changing working directory.

    Ref: http://stackoverflow.com/a/24176022
    """
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def run_command_under_r_root(cmd, catched=True):
    with cd(newdir='/Users/chairco/OneDrive/SourceCode/django/Qmonitor/enterprise/radars'):
        if catched:
            process = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            process = sp.run(cmd)
        return process


def r_etl(equipment, process='ETL', r='etl.R'):
    """
    :type equipment: str, ex:cvdu01, cvdu02
    :type process: str, ex:ETL, EHM
    :rtype: OrderedDict()
    """
    etl_proesses = OrderedDict()
    commands = OrderedDict([
        (process, [RScript, r, process, equipment]),
    ])
    for cmd_name, cmd in commands.items():
        etl_proesses[cmd_name] = run_command_under_r_root(cmd)
    time.sleep(3)
    return etl_proesses


def etl_task():
    group_id = async_chain([('radars.rtasks.r_etl', ('cvdu01', 'ETL')),
                            ('radars.rtasks.r_etl', ('cvdu02', 'ETL'))])#, group='ETL')
    return result_group(group_id, count=2)






