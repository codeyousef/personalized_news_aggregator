from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from unittest.mock import patch
from .models import Topic, Article


class TopicModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_topic_creation(self):
        topic = Topic.objects.create(name='technology', user=self.user)
        self.assertTrue(isinstance(topic, Topic))
        self.assertEqual(topic.name, 'technology')
        self.assertEqual(topic.user, self.user)


class ArticleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
        self.topic = Topic.objects.create(name='technology', user=self.user)
    
    def test_article_creation(self):
        article = Article.objects.create(
            title='Test Article',
            description='This is a test article',
            url='https://example.com/article',
            published_at=timezone.now(),
            source_name='Test Source',
            topic=self.topic
        )
        self.assertTrue(isinstance(article, Article))
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.topic, self.topic)


class TopicViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        self.add_topic_url = reverse('add_topic')
        self.my_topics_url = reverse('my_topics')
    
    def test_add_topic(self):
        response = self.client.post(self.add_topic_url, {'name': 'sports'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Topic.objects.filter(name='sports', user=self.user).exists())
    
    def test_my_topics(self):
        Topic.objects.create(name='technology', user=self.user)
        response = self.client.get(self.my_topics_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'technology')
    
    def test_remove_topic(self):
        topic = Topic.objects.create(name='technology', user=self.user)
        remove_topic_url = reverse('remove_topic', args=[topic.id])
        response = self.client.post(remove_topic_url)
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Topic.objects.filter(id=topic.id).exists())


class NewsFetchingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        self.topic = Topic.objects.create(name='technology', user=self.user)
        self.feed_url = reverse('feed')
    
    @patch('news.views.fetch_news_for_keyword')
    def test_news_fetching(self, mock_fetch):
        # Mock the API response
        mock_fetch.return_value = [{
            'title': 'Test Article',
            'description': 'Test Description',
            'url': 'https://example.com/article',
            'publishedAt': timezone.now().isoformat(),
            'source': {'name': 'Test Source'}
        }]
        
        # Test the feed view
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        
        # Check if the article was saved
        self.assertTrue(Article.objects.filter(title='Test Article').exists())