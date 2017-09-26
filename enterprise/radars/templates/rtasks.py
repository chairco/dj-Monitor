from collections import OrderedDict
from contextlib import contextmanager
import os
import subprocess as sp

from django_q.tasks import async, result
from django.conf import settings


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
    with cd(newdir=settings.enterprise):
        if catched:
            process = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            process = sp.run(cmd)
        return process



def r_etl():
    etl_proesses = OrderedDict()
    commands = OrderedDict([
        ('cvdu01', [RScript, 'ETL', 'cvdu01']),
    ])
    for cmd_name, cmd in commands.items():
        etl_proesses[cmd_name] = run_command_under_r_root(cmd)
    return etl_proesses



