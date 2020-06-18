from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from django_currentuser.db.models import CurrentUserField

from ckeditor.fields import RichTextField

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True)
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = CurrentUserField()

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}-{slugify(timezone.now().date())}'
        return super(Post, self).save(*args, **kwargs)