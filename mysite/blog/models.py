from django.db import models
from django.contrib.auth.forms import User
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    content = HTMLField(verbose_name=_("Content"), max_length=10000)
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)

    def comments_count(self):
        return self.comments.all().count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class Photo(models.Model):
    link = models.ImageField(verbose_name=_("Photo"), upload_to="photos")

    def __str__(self):
        return self.link.path

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")



class Comment(models.Model):
    post = models.ForeignKey(to="Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name=_("Content"), max_length=10000)
    author = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.date} ({self.author})"

    class Meta:
        ordering = ['-date']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Photo"), default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f'{self.user.username} {_("profile")}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.photo.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width) / 2
            bottom = (img.height + img.width) / 2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height) / 2
            right = (img.width + img.height) / 2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")