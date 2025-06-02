from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Главная страница
def test_page(request):
    context = {
        'current_time': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    }
    return render(request, 'index.html', context)

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