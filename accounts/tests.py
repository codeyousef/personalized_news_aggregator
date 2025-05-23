from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.test_user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )

    def test_user_registration(self):
        # Test user creation
        self.assertTrue(isinstance(self.test_user, User))
        
        # Test registration view with POST
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
    def test_user_login(self):
        # Test login view with POST
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_user_logout(self):
        # Login first
        self.client.login(username='testuser', password='testpassword123')
        
        # Test logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout