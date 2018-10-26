from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models.clasDict import classes
from blog.models.post import Post
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

NUM_OF_POSTS = 100
    
def home(request, username=None):
    post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    return render(request, 'blog/home.html', {'posts': posts,'classes':classes})
