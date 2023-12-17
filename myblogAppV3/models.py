from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helper import *


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    content = FroalaField()
    image = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)
    date_added = models.DateTimeField(default=timezone.now)
    upload_to = models.DateTimeField(auto_now=True)

    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)
