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
    if task.func == 'radars.rtasks.r_etl':
        etl = decode_cmd_out(result['815'])
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
        etl_groups.setdefault(idx + 1, decode_cmd_out(value['815']))
    return render(request, 'radars/etl_group.html', {
        'etl_groups': etl_groups,
    })


def etl(request):
    # Select orders in queue
    queue_orders = OrmQ.objects.all().order_by('lock')
    # Select finished orders
    complete_orders = Task.objects.all().filter(
        func__exact='radars.rtasks.r_etl',
    )

    paginator = Paginator(complete_orders, 10)
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
        if isinstance(context['object'].result, OrderedDict):
            context['object'].result = decode_cmd_out(
                context['object'].result['815'])
        else:
            print(context['object'].result)
        return context
