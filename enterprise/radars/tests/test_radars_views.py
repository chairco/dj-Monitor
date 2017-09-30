# radars/tests/test_radars_views.py
import pytest

from radars.views import TaskList


@pytest.mark.django_db
def test_TaskLists(rf):
    request = rf.get('/radars/t')
    response = TaskList.as_view()(request)
    assert response.status_code == 200


def test_815_index_Content(client):
    response = client.get('/radars/')
    assert response.content == b''
