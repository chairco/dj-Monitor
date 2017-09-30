# radar/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.etl, name='etl'),
    url(r'^tasks/$', views.TaskList.as_view(), name='task_list'),
    url(r'^tasks/detail/(?P<pk>\w+)$', views.TaskDetail.as_view(), name='task_detail'),
    url(r'^task/(?P<id>\w+)$', views.view_task, name='view_task'),
    url(r'^group/(?P<id>\w+)$', views.view_group, name='view_group'),
]