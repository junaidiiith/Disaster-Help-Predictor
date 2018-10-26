from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models.clasDict import classes
from blog.models.post import Post
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.models.comment import Comment
from blog.models.post import Post
from blog.models.clasDict import classes

@register.filter

def get_item(dictionary, key):
    return dictionary.get(key)
    
class PostClassView(generic.DetailView):
    model = Post
    template_name = 'blog/post_class.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(clss=self.kwargs['pk'])
        context['classes'] = classes
        return context