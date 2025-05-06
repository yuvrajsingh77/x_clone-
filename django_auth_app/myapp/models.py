from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model with unique email
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Tweet model with likes and retweets
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets', blank=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

# Comment model for tweets
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} commented on {self.tweet.id}"

# UserSettings model (linked one-to-one with User)
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    private_account = models.BooleanField(default=False)
    allow_tagging = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=True)
    font_size = models.CharField(max_length=20, default='Medium')

    def __str__(self):
        return f"{self.user.username}'s Settings"

    class Meta:
        verbose_name_plural = 'User Settings'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)