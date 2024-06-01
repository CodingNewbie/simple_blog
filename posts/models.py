from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", args=[self.id])
