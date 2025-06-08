import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskTracker.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from tasks.models import Task

def setup_permissions():
    try:
        # Получаем content_type для модели Task
        content_type = ContentType.objects.get_for_model(Task)
        
        # Получаем разрешения add_task и change_task
        add_permission = Permission.objects.get(content_type=content_type, codename='add_task')
        change_permission = Permission.objects.get(content_type=content_type, codename='change_task')
        
        # Создаем группу "Редакторы задач", если она не существует
        editors_group, created = Group.objects.get_or_create(name='Редакторы задач')
        
        # Добавляем разрешения в группу
        editors_group.permissions.add(add_permission, change_permission)
        
        # Находим пользователя admin и добавляем его в группу
        try:
            admin = User.objects.get(username='admin')
            admin.groups.add(editors_group)
            print(f'Пользователь {admin.username} добавлен в группу Редакторы задач')
        except User.DoesNotExist:
            print('Пользователь admin не найден')
        
        print('Группа "Редакторы задач" успешно настроена')
    except Exception as e:
        print(f'Ошибка при настройке разрешений: {e}')

if __name__ == '__main__':
    setup_permissions() 