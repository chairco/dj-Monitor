# radar/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^815/$', views.etl, name='etl'),
    url(r'^rate/$', views.exchangerate, name='rate'),
    url(r'^task/(?P<id>\w+)$', views.view_task, name='view_task'),
    url(r'^group/(?P<id>\w+)$', views.view_group, name='view_group'),
    url(r'^t/$', views.TaskList.as_view(), name='task_list'),
    url(r'^t/(?P<pk>\w+)$', views.TaskDetail.as_view(), name='task_detail'),
]