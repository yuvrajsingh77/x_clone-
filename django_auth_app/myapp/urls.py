from django.urls import path
from . import views

urlpatterns = [
    # Authentication Views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Core App Views
    path('', views.index_view, name='index'),
    path('explore/', views.explore_view, name='explore'),
    path('messages/', views.messages_view, name='messages'),
    path('settings/', views.settings_view, name='settings'),

    # Tweet Functionality
    path('post/', views.post_tweet, name='post_tweet'),
    path('like-tweet/<int:pk>/', views.like_tweet, name='like_tweet'),
    path('retweet/<int:pk>/', views.retweet, name='retweet'),
    path('comment/<int:pk>/', views.comment_tweet, name='comment_tweet'),
    path('like-tweet/<int:pk>/', views.like_tweet, name='like_tweet'),
    path('retweet/<int:pk>/', views.retweet, name='retweet'),
    path('comment/<int:pk>/', views.comment_tweet, name='comment_tweet'),
    path('delete-tweet/<int:pk>/', views.delete_tweet, name='delete_tweet'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('delete-tweet/<int:pk>/', views.delete_tweet, name='delete_tweet'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),


]

