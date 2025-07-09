from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile, Post, Follow, Comment, Like, Notification
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, ProfileForm
from django.contrib import messages
from django.http import HttpResponseForbidden

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
    
def home(request):
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        
        posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    else:
        posts = []

    return render(request, 'core/home.html', {'posts': posts})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'comment_form': CommentForm(),
    }
    return render(request, 'core/profile.html', context)

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('profile', username=username)

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    if not created:
        follow_obj.delete()
    else:
        Notification.objects.create(
            user=target_user,       
            actor=request.user,      
            type='follow'
        )

    return redirect('profile', username=username)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'core/post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            if post.user != request.user:
                Notification.objects.create(
                    user=post.user,       
                    actor=request.user,   
                    post=post,
                    type='comment'
                )
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'core/post_detail.html', context)

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete() 
    else:
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,      
                actor=request.user,  
                post=post,
                type='like'
            )
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def feed(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')

    for post in posts:
        post.is_liked = post.all_likes.filter(user=request.user).exists()
        post.comment_form = CommentForm()
        post.comments = post.all_comments.order_by('-created_at')[:3]
        post.is_following = Follow.objects.filter(follower=request.user, following=post.user).exists()
    return render(request, 'core/feed.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            # notification for comment
            if post.user != request.user:
                Notification.objects.create(
                    user=post.user,
                    actor=request.user,
                    type='comment',
                    post=post
                )
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def user_list(request):
    query = request.GET.get('q', '')  
    
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(username__icontains=query)
    
    following = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    context = {
        'users': users,
        'following': following,
        'query': query,
    }
    return render(request, 'core/user_list.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('feed')  

    return redirect('feed')

def base_context(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notification_count': unread_count}
    return {}

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    notifications.update(is_read=True)

    return render(request, 'core/notifications.html', {'notifications': notifications})
