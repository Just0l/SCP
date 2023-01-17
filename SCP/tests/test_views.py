from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from User.models import Workshop


class TestViewRespnses(TestCase):
    def setUp(self):
        self.c = Client()   
        self.user = Workshop.objects.create(
            username='testuser',
            password='testpassword'
        )

    def test_homepage_url(self):
        '''
        test homepage response status 
        '''

        response = self.c.get('/') 
        self.assertEqual(response.status_code, 200)

    
    def test_login_page(self):
        '''
        Test login page response status and template
        '''
        response = self.c.get(reverse('scp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'SCP/login.html')



    def test_form_valid(self):
        '''
        Test form validation, user role check and redirect
        '''
        response = self.c.post(reverse('scp:ws-login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('scp:workshop-home'))


    def test_redirect_ws(self):
        '''
        Test user role check and redirection to workshop-home page
        '''
        response = self.c.get(reverse('scp:workshop-home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('scp:workshop-home'))
