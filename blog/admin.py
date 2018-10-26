from django.contrib import admin

from blog.models.comment import Comment
from blog.models.post import Post
from blog.models.image import Image
from blog.models.help_request import Request


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Request)
