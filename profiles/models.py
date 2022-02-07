from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    biography = models.CharField(max_length=260, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class FollowRelation(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower} => {self.following}'
