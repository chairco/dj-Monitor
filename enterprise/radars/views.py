import logging

from collections import namedtuple, OrderedDict

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest, Http404, HttpResponse

from django_q.tasks import async, result, Task
from django_q.models import OrmQ
from django_q.humanhash import humanize
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


logger = logging.getLogger(__name__)


@require_GET
def view_task(request, id):
    task = get_object_or_404(Task, id=id)
    result = task.result
    if task.func == 'radars.tasks.order_fruit':
        return render(request, 'radars/task_detail.html', {
           'result': result,
        })
    if task.func == 'radars.tasks.get_exchangerate':
        if type(result) is type(OrderedDict()): 
            return render(request, 'radars/task_detail.html', {
                'ret': result['ret'],
                'status': result['status'],
                'values': result['values'],
                'version': result['version'],
                'result': result['get_exchangerate_job'],
            })
        else:
            return render(request, 'radars/task_detail.html', {
                'result': result,
            })
    raise Http404(
        'Given task of type %s does not have the result template '
        'to be rendered yet.'
        % task.func
    )


def home(request):
    if request.method == 'POST':
        # Parse the form params
        try:
            fruit = request.POST.get('fruit_type', '')
            num_fruit = int(request.POST.get('num_fruit', '1'))
        except ValueError:
            return HttpResponseBadRequest('Invalid fruit request!')
        # Create async task
        task_id = async(
            'radars.tasks.order_fruit',
            fruit=fruit, num_fruit=num_fruit
        )
        messages.info(
            request,
            'You ordered {fruit:s} x {num_fruit:d} (task: {task})'
            .format(fruit=fruit, num_fruit=num_fruit, task=humanize(task_id))
        )

    # Select orders in queue
    queue_orders = OrmQ.objects.all().order_by('lock')

    # Select finished orders
    complete_orders = Task.objects.all().filter(
        func__exact='radars.tasks.order_fruit',
    )
    return render(request, 'radars/home.html', {
        'queue_orders': queue_orders,
        'complete_orders': complete_orders
    })


def exchangerate(request):
    if request.method == 'POST':
        # Parse the form params
        # Create async task
        try:
            url = request.POST.get('url', '')
        except ValueError:
            return HttpResponseBadRequest('Invalid url request!')
        
        # Create async task
        task_id = async(
            'radars.tasks.get_exchangerate',
            url=url
        )
        messages.info(
            request,
            'start get exchangerate (task: {task})'
            .format(task=humanize(task_id))
        )

    # Select orders in queue
    queue_orders = OrmQ.objects.all().order_by('lock')

    # Select finished orders
    complete_orders = Task.objects.all().filter(
        func__exact='radars.tasks.get_exchangerate',
    )
    return render(request, 'radars/exchangerate.html', {
        'queue_orders': queue_orders,
        'complete_orders': complete_orders
    })


def etl(request):
    pass