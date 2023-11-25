# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:user>/', views.profile, name='profile'),
    path('post/', views.upload_post.as_view(), name='upload_post'),
    path('profile/edit/<str:user>/', views.profile_update.as_view(), name='update_profile'),
    path('follow_request/', views.follow_unfollow, name='follow_unfollow'),
    path('load_follow/', views.load_followers_following, name="load_followers_following"),
    path('load_posts/', views.load_posts, name="load_posts"),
    path('post/<int:pk>', views.load_whole_post, name="load_whole_post")
]
