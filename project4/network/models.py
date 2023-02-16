import math
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp
        }
    
    def __str__(self):
        return f'{self.author}: {self.body}'

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"
    
        elif diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        elif diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        elif diff.days >= 1 and diff.days < 5:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
        
        else:
            return self.timestamp.strftime("%b %d %Y, %I:%M %p")


class Follow(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='being_followed')

    def __str__(self):
        return f'{self.user} -> {self.following}'


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_liked')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_liked')

    def __str__(self):
        return f'{self.user} -> {self.post}'