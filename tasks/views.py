from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .forms import UserRegisterForm, TaskForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Task
import json
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

# Главная страница
def index_page(request):
    # Получаем параметр фильтра из GET-запроса
    filter_type = request.GET.get('filter', 'pending')
    
    # Фильтруем задачи в зависимости от выбранного фильтра
    if filter_type == 'completed':
        tasks = Task.objects.filter(status='completed').order_by('-created_at')
    elif filter_type == 'all':
        tasks = Task.objects.all().order_by('-created_at')
    else:  # по умолчанию показываем невыполненные
        tasks = Task.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'current_time': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        'tasks': tasks,
        'form': TaskForm() if request.user.is_authenticated else None,
        'current_filter': filter_type
    }
    return render(request, 'index.html', context)

@login_required
@permission_required('tasks.add_task', raise_exception=True)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('test_page')
    return redirect('test_page')

@login_required
@permission_required('tasks.change_task', raise_exception=True)
def complete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
    except Task.DoesNotExist:
        messages.error(request, 'Задача не найдена!')
    return redirect('test_page')

@require_http_methods(["POST"])
@login_required
@permission_required('tasks.change_task', raise_exception=True)
def complete_tasks(request):
    try:
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])
        
        if not task_ids:
            return JsonResponse({'success': False, 'error': 'Не выбраны задачи'})
            
        # Обновляем статус выбранных задач
        Task.objects.filter(
            id__in=task_ids,
            status='pending'
        ).update(
            status='completed',
            completed_at=timezone.now()
        )
        
        return JsonResponse({'success': True})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный формат данных'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Регистрация пользователей
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_success')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Успешная регистрация
def register_success(request):
    return render(request, 'register_success.html')

# Представление для входа
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('test_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Представление для выхода
def logout_view(request):
    logout(request)
    return redirect('test_page') 