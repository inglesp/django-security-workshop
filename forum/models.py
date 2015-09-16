from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    owner = models.ForeignKey(User)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post by {} at {}'.format(self.owner.username, self.created_at)
