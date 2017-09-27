import logging

from collections import namedtuple, OrderedDict

from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib import messages
from django.http import HttpResponseBadRequest, Http404, HttpResponse

from django_q.tasks import async, result, Task, result_group
from django_q.models import OrmQ
from django_q.humanhash import humanize
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, ListView, DetailView, UpdateView


logger = logging.getLogger(__name__)


ParsedCompletedCommand = namedtuple(
    'ParsedCompletedCommand',
    ['returncode', 'args', 'stdout', 'stderr'])


def decode_cmd_out(completed_cmd):
    try:
        stdout = completed_cmd.stdout.decode()
    except AttributeError:
        stdout = '<EMPTY>'
    try:
        stderr = completed_cmd.stderr.decode()
    except AttributeError:
        stderr = '<EMPTY>'
    return ParsedCompletedCommand(
        completed_cmd.returncode,
        completed_cmd.args,
        stdout,
        stderr
    )


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
    if task.func == 'radars.rtasks.r_etl':
        etl = decode_cmd_out(result['ETL'])
        return render(request, 'radars/etl_detail.html', {
            'etl': etl,
        })

    raise Http404(
        'Given task of type %s does not have the result template '
        'to be rendered yet.'
        % task.func
    )


@require_GET
def view_group(request, id):
    task = get_object_or_404(Task, id=id)
    groups = result_group(task.group)
    etl_groups = {}
    for idx, value in enumerate(reversed(groups)):
        etl_groups.setdefault(idx + 1, decode_cmd_out(value['ETL']))

    return render(request, 'radars/etl_group.html', {
        'etl_groups': etl_groups,
    })


class TaskList(ListView):
    """Displays the lists of a task"""
    model = Task
    template_name = 'radars/tasks_list.html'


class TaskDetail(DetailView):
    """Displays the details of a task"""
    model = Task
    template_name = 'radars/tasks_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['object'].result = decode_cmd_out(
            context['object'].result['ETL'])
        return context


def etl(request):
    # Select orders in queue
    queue_orders = OrmQ.objects.all().order_by('lock')
    # Select finished orders
    complete_orders = Task.objects.all().filter(
        func__exact='radars.rtasks.r_etl',
    )

    paginator = Paginator(complete_orders, 5)
    page = request.GET.get('page')

    try:
        complete_orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        complete_orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        complete_orders = paginator.page(paginator.num_pages)

    return render(request, 'radars/etl.html', {
        'queue_orders': queue_orders,
        'complete_orders': complete_orders
    })


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