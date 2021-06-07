from django.contrib.auth.models import User
from django.db import models



class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)


    class Meta:
        ordering = ['created']

class Like(models.Model):
    owner = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE, null=True, blank=True)
    likes_number = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.post}-->{self.owner}"


class DisLike(models.Model):
    owner = models.OneToOneField('auth.User', related_name='dis_likes', on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post, related_name="dis_likes", on_delete=models.CASCADE, null=True, blank=True)
    dislikes_number = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.post}-->{self.owner}"






