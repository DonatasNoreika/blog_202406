from django.db import models
from django.contrib.auth.forms import User
from tinymce.models import HTMLField

# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100)
    content = HTMLField(verbose_name="Content", max_length=10000)
    date = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)

    def comments_count(self):
        return self.comments.all().count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    link = models.ImageField(verbose_name="Photo", upload_to="photos")


class Comment(models.Model):
    post = models.ForeignKey(to="Post", verbose_name="Post", on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Content", max_length=10000)
    author = models.ForeignKey(to=User, verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(verbose_name="Date", auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.date} ({self.author})"

    class Meta:
        ordering = ['-date']