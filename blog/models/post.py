from django.db import models
from django.urls import reverse
from blog.models import clasDict

class Post(models.Model):
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    clss = models.IntegerField()
    location = models.TextField()

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def __str__(self):
        return '{body} by {clss}'.format(body=self.body,
                                                clss=clasDict.classes[self.clss])
