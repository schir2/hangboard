from django.shortcuts import render
from django.urls import reverse

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name_suffix = '_list'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name_suffix = '_detail'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content')
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('post_detail', args=(self.object.slug,))


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content')
    template_name_suffix = '_form'

    def get_success_url(self):
        return reverse('post_detail', args=(self.object.slug,))


class PostDeleteView(DeleteView):
    model = Post
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('post_list')