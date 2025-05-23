from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import requests
import os
from .models import Topic, Article
from .forms import TopicForm


def fetch_news_for_keyword(keyword):
    """Fetch news articles from NewsAPI for a given keyword."""
    api_key = os.environ.get('NEWS_API_KEY', 'dummy_api_key_for_testing')
    url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={api_key}"
    
    # For testing purposes, we'll simulate a response
    if api_key == 'dummy_api_key_for_testing':
        return [{
            'title': f'Test Article about {keyword}',
            'description': f'This is a test article about {keyword}',
            'url': f'https://example.com/article/{keyword}',
            'publishedAt': timezone.now().isoformat(),
            'source': {'name': 'Test Source'}
        }]
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []


def save_articles(articles_data, topic_obj):
    """Save article data to the database, avoiding duplicates."""
    for article_data in articles_data:
        # Check if the article already exists
        article_url = article_data.get('url')
        if not Article.objects.filter(url=article_url).exists():
            Article.objects.create(
                title=article_data.get('title', ''),
                description=article_data.get('description', ''),
                url=article_url,
                published_at=article_data.get('publishedAt', timezone.now()),
                source_name=article_data.get('source', {}).get('name', 'Unknown'),
                topic=topic_obj
            )


@login_required
def feed(request):
    """Display personalized news feed for the logged-in user."""
    # Get all topics for the current user
    user_topics = Topic.objects.filter(user=request.user)
    
    # Get or fetch articles for each topic
    articles = []
    for topic in user_topics:
        # First check if we have recent articles for this topic
        recent_articles = Article.objects.filter(
            topic=topic, 
            created_at__gte=timezone.now() - timedelta(days=1)
        )
        
        if not recent_articles.exists():
            # If no recent articles, fetch new ones
            fetched_articles = fetch_news_for_keyword(topic.name)
            save_articles(fetched_articles, topic)
        
        # Get all articles for this topic
        topic_articles = Article.objects.filter(topic=topic)
        articles.extend(topic_articles)
    
    # Sort all articles by published date
    articles.sort(key=lambda x: x.published_at, reverse=True)
    
    return render(request, 'news/feed.html', {'articles': articles})


@login_required
def add_topic(request):
    """Add a new topic for the current user."""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # Create the topic but don't save it yet
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            
            # Fetch articles for this new topic
            articles = fetch_news_for_keyword(topic.name)
            save_articles(articles, topic)
            
            return redirect('my_topics')
    else:
        form = TopicForm()
    
    return render(request, 'news/add_topic.html', {'form': form})


@login_required
def my_topics(request):
    """Display all topics for the current user."""
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'news/my_topics.html', {'topics': topics})


@login_required
def remove_topic(request, topic_id):
    """Remove a topic and all associated articles."""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the topic (and associated articles due to CASCADE)
        topic.delete()
        return redirect('my_topics')
    
    return render(request, 'news/confirm_delete_topic.html', {'topic': topic})