import os
import subprocess as sp
import time
import logging
import sys

from collections import OrderedDict
from contextlib import contextmanager

from django_q.tasks import async, result, async_chain, result_group
from django.conf import settings

from query.equip import FDA


RScript = settings.R_BIN
R_PATH = settings.R_PATH


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
    with cd(newdir=R_PATH):
        if catched:
            process = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            process = sp.run(cmd)
        return process


def r_etl(equipment, process, r='Analysis_Main.R', project='815'):
    """
    :type equipment: str, ex:cvdu01, cvdu02
    :type process: str, ex:ETL, EHM
    :rtype: OrderedDict()
    """
    etl_proesses = OrderedDict()
    commands = OrderedDict([
        (project, [RScript, r, process, equipment]),
    ])
    for cmd_name, cmd in commands.items():
        etl_proesses[cmd_name] = run_command_under_r_root(cmd)
    return etl_proesses


def delete_duplicates(tasks):
    """
    :type tasks: list()
    :rtype = list()
    """
    ret = []
    for task in tasks:
        if task not in ret:
            ret.append(task)
    return ret


def get_task(equipment):
    """
    :type equipment: str
    :rtype: list()
    """
    tasks = ['ETL'] # should be exist ETL
    task_mapping = {
        'FDC_Import': 'ETL',
        'FDC_Indicator': 'ETL',
        'FDC_Sync': 'ETL',
        'Mea_Import': 'ETL',
        'EHM_Process': 'EHM',
        'AVM_Process': 'AVM',
        'XSPC_Process': 'XSPC',
        'AVM_Product': 'AVM_Batch',
        'SPC_Product': 'SPC'
    }
    fda = FDA()
    fda.equipment = equipment
    rows = [row[0] for row in fda.get_lastendtime() if row[1] == True]
    for k, v in task_mapping.items():
        if k in rows:
            tasks.append(v)
            rows.remove(k)
    tasks = delete_duplicates(tasks=tasks)
    return tasks


def etl_task(equipment):
    """
    :type equipment: str
    :rtype: QuerySet()
    """
    tasks = get_task(equipment=equipment)
    chains = [('radars.rtasks.r_etl', (equipment, task)) for task in tasks]
    group_id = async_chain(chains)
    return result_group(group_id, count=len(tasks))

