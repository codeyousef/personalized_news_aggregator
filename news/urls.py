from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('my_topics/', views.my_topics, name='my_topics'),
    path('remove_topic/<int:topic_id>/', views.remove_topic, name='remove_topic'),
]