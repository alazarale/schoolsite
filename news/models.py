from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class News(models.Model):
    owner = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='news/images')
    selected = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text[:15]


class CommentReply(models.Model):
    user = models.ForeignKey(User, related_name='comment_reply', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name='comment_reply', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text[:10]

