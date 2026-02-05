from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from datetime import timedelta
import json


def dashboard(request):
    # 1. Base Query
    active_tasks = Task.objects.filter(is_deleted=False)

    # 2. Stats Counters (Unchanged)
    total_tasks = active_tasks.count()
    completed_tasks = active_tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    # 3. SORTING LOGIC FOR RECENT TASKS
    sort_by = request.GET.get('sort', 'newest')  # Default to newest

    if sort_by == 'urgency':
        # Sort by due date (soonest first), nulls last
        recent_tasks = active_tasks.order_by(F('due_date').asc(nulls_last=True))[:5]
    elif sort_by == 'updated':
        # Recently updated
        recent_tasks = active_tasks.order_by('-updated_at')[:5]
    else:
        # Default: Recently Created
        recent_tasks = active_tasks.order_by('-created_at')[:5]

    # 4. CHART LOGIC (Unchanged)
    today = timezone.now().date()
    chart_labels = []
    chart_data = []

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        label = date.strftime("%a")
        chart_labels.append(label)
        daily_count = Task.objects.filter(
            is_completed=True,
            is_deleted=False,
            updated_at__date=date
        ).count()
        chart_data.append(daily_count)

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_tasks': recent_tasks,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'current_sort': sort_by,  # Pass sorting status to template
    }

    return render(request, 'dashboard.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    # We pass 'page_title' and 'btn_text' to the template
    context = {
        'form': form,
        'page_title': 'New Task',
        'page_subtitle': 'What do you need to get done?',
        'btn_text': 'Create Task'
    }
    return render(request, 'task_form.html', context)


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    # Same template, different text!
    context = {
        'form': form,
        'page_title': 'Edit Task',
        'page_subtitle': 'Update your plans.',
        'btn_text': 'Save Changes'
    }
    return render(request, 'task_form.html', context)


def soft_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_deleted = True
    task.save()
    return redirect('dashboard')


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # SOFT DELETE: Only marks it as deleted
    task.is_deleted = True
    task.save()

    return redirect('dashboard')


def trash_bin(request):
    # Only show tasks where is_deleted is True
    deleted_tasks = Task.objects.filter(is_deleted=True).order_by('-created_at')
    return render(request, 'trash.html', {'tasks': deleted_tasks})

def permanent_delete(request, pk):
    # This actually removes the record from the SQLite database
    task = get_object_or_404(Task, pk=pk, is_deleted=True)
    task.delete()
    return redirect('trash_bin')


def restore_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Bring it back to the dashboard
    task.is_deleted = False
    task.save()

    return redirect('trash_bin')


def delete_forever(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # actually delete from database
    task.delete()

    return redirect('trash_bin')


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Toggle the status (if it's done, make it pending, and vice versa)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('dashboard')

def task_list(request):
    # 1. Get parameters from URL (defaults: status='all', sort='newest')
    status = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', 'newest')

    # 2. Base Query
    tasks = Task.objects.filter(is_deleted=False)

    # 3. Apply Filtering
    page_title = "All Tasks"
    if status == 'completed':
        tasks = tasks.filter(is_completed=True)
        page_title = "Completed Tasks"
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)
        page_title = "In Progress Tasks"

    # 4. Apply Sorting
    if sort_by == 'urgency':
        # Sort by due date (soonest first). Put tasks with no due date at the bottom.
        from django.db.models import F
        tasks = tasks.order_by(F('due_date').asc(nulls_last=True))
    elif sort_by == 'updated':
        tasks = tasks.order_by('-updated_at') # Most recently changed
    else:
        tasks = tasks.order_by('-created_at') # Newest created (default)

    context = {
        'tasks': tasks,
        'page_title': page_title,
        'current_status': status,
        'current_sort': sort_by
    }
    return render(request, 'task_list.html', context)