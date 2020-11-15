from django.db import models

from django.contrib.auth.models import User


# Make the main class model to keep user posts
class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


# Make a vote model to keep a reference to a user and a post
# Who made the vote and what did they vote for value
# This will ensure that someone cant vote on same post over and over
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
