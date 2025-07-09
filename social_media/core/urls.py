
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('feed/', views.feed, name='feed'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('users/', views.user_list, name='user_list'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('notifications/', views.notifications_view, name='notifications'),

]
