from django.contrib.auth.models import User
from django.db import models

from blog.models.post import Post
CHOICES = [
    (1, "Caution/Advice"),
    (2, "Damage"),
    (3, "Disease"),
    (4, "Information"),
    (5, "Need Help"),
    (6, "Other"),
    (7, "People Affected"),
    (8, "Support")]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return '"{body}..." on {post_title} by {username}'.format(body=self.vote,
                                                                  post_title=self.post.title,
                                                                  username=self.user.username)
