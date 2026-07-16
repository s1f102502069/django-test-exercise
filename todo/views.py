from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task


def index(request):
    if request.method == 'POST':
        due_at_raw = request.POST.get('due_at', '').strip()
        parsed_due_at = parse_datetime(due_at_raw) if due_at_raw else None
        due_at = make_aware(parsed_due_at) if parsed_due_at else None

        task = Task(title=request.POST['title'], due_at=due_at)
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def edit(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/edit.html', context)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.delete()
    return redirect('/')


def toggle_completed(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method != 'POST':
        return redirect('detail', task_id=task.pk)

    task.completed = not task.completed
    task.save()
    return redirect('detail', task_id=task.pk)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        due_at_value = request.POST.get('due_at')
        if due_at_value:
            task.due_at = make_aware(parse_datetime(due_at_value))
        else:
            task.due_at = None
        task.save()
        return redirect('detail', task_id=task.pk)

    return redirect('edit', task_id=task.pk)
