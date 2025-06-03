from django.urls import path
from . import views

urlpatterns = [
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('complete-tasks/', views.complete_tasks, name='complete_tasks'),
] 