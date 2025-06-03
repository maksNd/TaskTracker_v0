from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .forms import UserRegisterForm, TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task

# Главная страница
def test_page(request):
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
def complete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'completed'
        task.save()
    except Task.DoesNotExist:
        messages.error(request, 'Задача не найдена!')
    return redirect('test_page')

# Регистрация пользователей
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для пользователя {username}!')
            return redirect('register_success')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Успешная регистрация
def register_success(request):
    return render(request, 'register_success.html') 