from django.urls import path

from blog.views.comment import CommentCreate
from blog.views.home import home
from blog.views.post import PostView, PostCreate, PostUpdate, PostDelete
from blog.views.help_requests import help_requests, RequestView
from blog.views.findmissing import findMissing,results
from blog.views.post_cls import PostClassView 


app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    path('', home, name='home'),
    path('findMissing', findMissing, name='find-missing'),
    path('results', results, name='myresults'),
    # # ex: /blog/dusan
    path('helprequests', help_requests, name='help-requests'),
    path('dclass/<int:pk>', PostClassView.as_view(), name='post_clas'),

    path('requests/<int:pk>', RequestView.as_view(), name='request'),

    # path('',accept_volunteering, name='accept_volunteering')
    # path('',reject_volunteering, name='reject_volunteering')
    # ex: /blog/post/5/
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    # ex: /blog/post/5/comment/
    path('post/<int:pk>/comment/', CommentCreate.as_view(), name='create_comment')
]
