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

    path('follow_user/', views.follow_user, name='follow_user'),
    
    path('post/<int:pk>/', views.view_post, name="view_post"),
    path('post_like/', views.like_post, name='like_post'),
    path('delete_post/<int:pk>', views.delete_post, name="delete_post"),

    path('add_comment/', views.add_comment, name="add_comment"),
    path('delete_comment/<int:comment_pk>/<int:post_pk>/', views.delete_comment, name="delete_comment"),
]
