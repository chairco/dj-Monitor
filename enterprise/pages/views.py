import logging
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django_q.humanhash import humanize
from django_q.models import OrmQ
from django_q.tasks import async, Task

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')
