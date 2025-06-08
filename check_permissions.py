import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskTracker.settings')
django.setup()

from django.contrib.auth.models import User

def check_permissions():
    try:
        # Проверяем права админа
        admin = User.objects.get(username='admin')
        print(f"User: {admin.username}")
        print(f"can_create_task: {admin.has_perm('tasks.can_create_task')}")
        print(f"can_edit_task: {admin.has_perm('tasks.can_edit_task')}")
        
        # Проверяем права тестового пользователя
        testuser = User.objects.get(username='testuser')
        print(f"\nUser: {testuser.username}")
        print(f"can_create_task: {testuser.has_perm('tasks.can_create_task')}")
        print(f"can_edit_task: {testuser.has_perm('tasks.can_edit_task')}")
    except User.DoesNotExist as e:
        print(f"User not found: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_permissions() 