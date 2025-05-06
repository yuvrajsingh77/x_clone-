from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tweet, UserSettings

User = get_user_model()

# Home Page
@login_required
def index_view(request):
    tweets = Tweet.objects.select_related('user').order_by('-created_at')
    trending = ["#Django", "#Python", "#100DaysOfCode"]
    return render(request, 'index.html', {
        'tweets': tweets,
        'trending': trending
    })

# Explore Page
@login_required
def explore_view(request):
    return render(request, 'explore.html')

# Messages Page
@login_required
def messages_view(request):
    return render(request, 'messages.html')

# ✅ Settings Page with Account Update
@login_required
def settings_view(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update settings preferences
        settings.private_account = bool(request.POST.get('private_account'))
        settings.allow_tagging = bool(request.POST.get('allow_tagging'))
        settings.email_notifications = bool(request.POST.get('email_notifications'))
        settings.push_notifications = bool(request.POST.get('push_notifications'))
        settings.dark_mode = bool(request.POST.get('dark_mode'))
        settings.font_size = request.POST.get('font_size', 'Medium')
        settings.save()

        # Update username and password
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')








        if new_username and new_username != request.user.username:
            request.user.username = new_username

        if new_password:
            request.user.set_password(new_password)

        request.user.save()

        # Re-authenticate if password changed
        if new_password:
            login(request, request.user)

        messages.success(request, "Settings saved successfully!")
        return redirect('settings')

    return render(request, 'settings.html', {
        'settings': settings,
        'user': request.user
    })

# ✅ Login View (Supports Email or Username)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'login.html', {
        'form_type': 'login'
    })

# ✅ Registration View (UserSettings created by signal)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # ❌ Removed: UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome 🎉')
            return redirect('index')

    return render(request, 'login.html', {
        'form_type': 'register'
    })

# ✅ Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

# ✅ Post Tweet View
@login_required
def post_tweet(request):
    if request.method == 'POST':
        content = request.POST.get('tweet', '').strip()
        if content:
            Tweet.objects.create(user=request.user, content=content)
            messages.success(request, 'Tweet posted!')
        else:
            messages.error(request, 'Tweet cannot be empty.')
    return redirect('index')
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, Comment
import json

@login_required
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': tweet.likes.count()
    })

@login_required
def retweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    if tweet.retweets.filter(id=request.user.id).exists():
        tweet.retweets.remove(request.user)
        reposted = False
    else:
        tweet.retweets.add(request.user)
        reposted = True
    
    return JsonResponse({
        'success': True,
        'reposted': reposted,
        'retweet_count': tweet.retweets.count()
    })

@login_required
def comment_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    data = json.loads(request.body)
    comment_text = data.get('comment', '')
    
    if comment_text.strip():
        comment = Comment.objects.create(
            user=request.user,
            tweet=tweet,
            content=comment_text
        )
        
        return JsonResponse({
            'success': True,
            'comment_count': tweet.comments.count(),
            'username': request.user.username,
            'comment': comment.content
        })
    
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, Comment
import json

@login_required
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': tweet.likes.count()
    })

@login_required
def retweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    if tweet.retweets.filter(id=request.user.id).exists():
        tweet.retweets.remove(request.user)
        reposted = False
    else:
        tweet.retweets.add(request.user)
        reposted = True
    
    return JsonResponse({
        'success': True,
        'reposted': reposted,
        'retweet_count': tweet.retweets.count()
    })

@login_required
def comment_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    data = json.loads(request.body)
    comment_text = data.get('comment', '')
    
    if comment_text.strip():
        comment = Comment.objects.create(
            user=request.user,
            tweet=tweet,
            content=comment_text
        )
        
        return JsonResponse({
            'success': True,
            'comment_count': tweet.comments.count(),
            'username': request.user.username,
            'comment': comment.content
        })
    
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    # Check if the user is the owner of the tweet
    if tweet.user != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
    tweet.delete()
    return JsonResponse({'success': True})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    tweet_id = comment.tweet.id
    
    # Check if the user is the owner of the comment
    if comment.user != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
    comment.delete()
    
    # Get the updated comment count
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comment_count = tweet.comments.count()
    
    return JsonResponse({'success': True, 'comment_count': comment_count})
@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    # Check if the user is the owner of the tweet
    if tweet.user != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
    tweet.delete()
    return JsonResponse({'success': True})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    tweet_id = comment.tweet.id
    
    # Check if the user is the owner of the comment
    if comment.user != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
    comment.delete()
    
    # Get the updated comment count
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comment_count = tweet.comments.count()
    
    return JsonResponse({'success': True, 'comment_count': comment_count})
