from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Article
from .serializers import ArticleSerializer

User = get_user_model()


#test registration
class RegisterTestCase(APITestCase):

    def test_register_with_short_password(self):
        data ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': '123456u',
            'password2': '123456u'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_only_digits_password(self):
        data ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': '12345678',
            'password2': '12345678'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_only_letter_password(self):
        data ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'asdfasdf',
            'password2': 'asdfasdf'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_bad_second_password(self):
        data ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'asdfasdf',
            'password2': 'asdfasdf1'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_bad_email(self):
        data ={
            'name': 'Test',
            'email': 'test@testcom',
            'password': 'asdfasdf1',
            'password2': 'asdfasdf1'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register(self):
        data ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'asdfasdf1',
            'password2': 'asdfasdf1'
        }
        url = reverse('register-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_notunique_email(self):
        data1 ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'asdfasdf1',
            'password2': 'asdfasdf1'
        }
        url = reverse('register-list')
        response1 = self.client.post(url, data=data1)
        data2 ={
            'name': 'Test',
            'email': 'test@test.com',
            'password': 'asdfasdf1',
            'password2': 'asdfasdf1'
        }
        url = reverse('register-list')
        response2 = self.client.post(url, data=data2)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


#test author permissions
class AuthorTestCase(APITestCase):
    
    def setUp(self):
        self.author = User.objects.create(email='test@test.com', is_author=True)
        self.user = User.objects.create(email='test1@test.com', is_author=False)

    def test_create_article_ok(self):
        data ={
            'title': 'Test',
            'content': 'Test post',
        }
        url = reverse('article-list')
        self.client.force_authenticate(self.author)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = data ={
            'title': 'Test',
            'content': 'Test post',
            'is_public': False
        }
        self.assertDictEqual(response.data, data)
    
    def test_create_article_by_user(self):
        data ={
            'title': 'Test',
            'content': 'Test post',
        }
        url = reverse('article-list')
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#test article owner permissions
class OwnerTestCase(APITestCase):
    
    def setUp(self):
        self.owner = User.objects.create(email='test@test.com', is_author=True)
        self.user = User.objects.create(email='test1@test.com', is_author=True)
        self.article = Article.objects.create(title='Owner test', content='Test', author=self.owner)

    def test_update_article_ok(self):
        data ={
            'title': 'New title',
            'content': 'Test post',
        }
        url = reverse('article-detail', args=(self.article.id,))
        self.client.force_authenticate(self.owner)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = data ={
            'title': 'New title',
            'content': 'Test post',
            'is_public': False
        }
        self.assertDictEqual(response.data, data)
    
    def test_update_article_by_not_owner(self):
        data ={
            'title': 'New title',
            'content': 'Test post',
        }
        url = reverse('article-detail', args=(self.article.id,))
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#test subscriber 
class SubscriberTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create(email='test@test.com', is_author=True)
        self.sub = User.objects.create(email='test1@test.com', is_subscriber=True)
        self.not_sub = User.objects.create(email='test2@test.com', is_subscriber=False)
        self.article1 = Article.objects.create(title='FOR SUBS', content='Test', author=self.owner)
        self.article2 = Article.objects.create(title='FOR ALL', content='Test', author=self.owner, is_public=True)
    
    def test_articles_for_subs(self):
        url = reverse('article-list')
        self.client.force_authenticate(self.sub)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ArticleSerializer([self.article2, self.article1], many=True).data
        self.assertEqual(expected_data, response.data)
    
    def test_articles_for_anon(self):
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ArticleSerializer([self.article2], many=True).data
        self.assertEqual(expected_data, response.data)
    
    def test_articles_for_not_sub_user(self):
        url = reverse('article-list')
        self.client.force_authenticate(self.not_sub)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ArticleSerializer([self.article2], many=True).data
        self.assertEqual(expected_data, response.data)
        
