from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models.clasDict import classes
from blog.models.post import Post
from blog.models.volunteer import Volunteer
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    
NUM_OF_POSTS = 5


def accept_volunteering(request):
    post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    Volunteer(person=request.session.user).save()

    return render(request, 'blog/home.html', {'posts': posts,'classes':classes,"message": "Thanks for volunteering"})

def reject_volunteering(request):
    post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    return render(request, 'blog/home.html', {'posts': posts,'classes':classes})
