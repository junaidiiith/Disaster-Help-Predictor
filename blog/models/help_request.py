from django.db import models
from django.urls import reverse
from blog.models import clasDict, post
from django.contrib.auth.models import User
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    

CHOICES = [(1,"Pending"), (2, "Assigned"), (3, "Resolved")]

class Request(models.Model):
    body = models.ForeignKey(post.Post, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    status = models.IntegerField(choices=CHOICES,default=CHOICES[0][0])
    resolution = models.TextField()

    def get_absolute_url(self):
        return reverse('blog:   request', kwargs={'pk': self.pk})

    def __str__(self):
        return '{body} by {clss}'.format(body=self.body)
