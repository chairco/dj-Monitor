# radars/tests/test_query.py
import pytest

from query.equip import FDA

from radars.rtasks import delete_duplicates, get_task


def test_duplicate():
    data1 = ['ETL', 'ETL', 'EHM', 'AVM']
    data2 = ['ETL', 'EHM', 'AVM', 'AVM']
    test_set = [data1, data2]
    correct = ['ETL', 'EHM', 'AVM']
    for task in test_set:
        tasks = delete_duplicates(tasks=task)
        assert tasks == correct


def test_get_task_count():
    task = get_task('cvdu01')
    assert len(task) >= 2


def test_get_task_order():
    task = get_task('cvdu01')
    assert task == ['ETL', 'EHM', 'XSPC'] # only 3, 2 has mark