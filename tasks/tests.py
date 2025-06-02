from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UrlsTestCase(TestCase):
    """Тесты для проверки доступности URL-адресов"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Создаем тестовый клиент
        self.client = Client()
    
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('test_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_register_page(self):
        """Тест страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_register_success_page(self):
        """Тест страницы успешной регистрации"""
        response = self.client.get(reverse('register_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_success.html')
    
    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_logout_page_post(self):
        """Тест страницы выхода через POST запрос"""
        # Сначала входим
        self.client.login(username='testuser', password='testpassword')
        # Затем выходим с помощью POST запроса и проверяем
        response = self.client.post(reverse('logout'))
        # Django's LogoutView перенаправляет по умолчанию
        self.assertEqual(response.status_code, 302)
    
    def test_logout_page_get(self):
        """Тест что GET запрос к странице выхода не разрешен"""
        # Сначала входим
        self.client.login(username='testuser', password='testpassword')
        # Пробуем выйти с помощью GET запроса
        response = self.client.get(reverse('logout'))
        # Должен вернуть код 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_admin_page_redirect_for_anonymous(self):
        """Тест редиректа анонимного пользователя с админки"""
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 404)
        # Должен быть редирект на страницу входа для админки
        self.assertEqual(response.status_code, 302)

class UserRegistrationTestCase(TestCase):
    """Тесты для функциональности регистрации пользователей"""
    
    def setUp(self):
        self.client = Client()
    
    def test_user_registration(self):
        """Тест процесса регистрации пользователя"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'simplepassword',
            'password2': 'simplepassword',
        })
        
        # Проверяем, что был редирект после успешной регистрации
        self.assertEqual(response.status_code, 302)
        
        # Проверяем, что пользователь был создан
        self.assertTrue(User.objects.filter(username='newuser').exists())

class UserAuthenticationTestCase(TestCase):
    """Тесты для функциональности аутентификации пользователей"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
    
    def test_user_login(self):
        """Тест входа пользователя"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        
        # Проверяем, что был редирект после успешного входа
        self.assertEqual(response.status_code, 302)
        
        # Проверяем, что пользователь авторизован
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
    
    def test_user_logout(self):
        """Тест выхода пользователя"""
        # Сначала входим
        self.client.login(username='testuser', password='testpassword')
        
        # Затем выходим с помощью POST запроса
        response = self.client.post(reverse('logout'))
        
        # Проверяем, что после выхода происходит редирект
        self.assertEqual(response.status_code, 302) 