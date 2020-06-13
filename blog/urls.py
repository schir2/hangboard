from django.urls import path

from blog.views import PostDetailView
from blog.views import PostListView
from blog.views import PostCreateView
from blog.views import PostUpdateView
from blog.views import PostDeleteView


urlpatterns = [
    path('posts/', PostListView.as_view(), name ='post_list'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('posts/<slug:slug>/edit', PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete', PostDeleteView.as_view(), name='post_delete'),
]