"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (search,
                    register,
                    profile,
                    PostListView,
                    PostDetailView,
                    UserPostListView,
                    UserCommentListView,
                    PostCreateView)

urlpatterns = [
    path("search/", search, name="search"),
    path("usercomments/", UserCommentListView.as_view(), name="user_comments"),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('', PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', PostDetailView.as_view(), name="post"),
    path("userposts/", UserPostListView.as_view(), name="user_posts"),
    path("posts/new", PostCreateView.as_view(), name="post_new"),
]
