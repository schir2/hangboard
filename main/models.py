from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


# Create your models here.


class SimpleModel(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    custom = models.BooleanField(default=True)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if not self.description:
            self.description = self.name
        super().save(*args, *kwargs)

    class Meta:
        abstract = True


class Material(SimpleModel):
    pass


class HoldType(SimpleModel):
    pass


class Exercise(SimpleModel):
    pass


class Hangboard(SimpleModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class Hold(SimpleModel):
    hangboard = models.ForeignKey(Hangboard, on_delete=models.CASCADE)
    hold_type = models.ForeignKey(HoldType, on_delete=models.CASCADE)
    size = models.IntegerField(default=20, null=True, blank=True)
    default_fingers = models.IntegerField(default=4)


class WorkoutSet(SimpleModel):
    hold = models.ForeignKey(Hold, on_delete=models.CASCADE)
    fingers = models.IntegerField(default=4)
    rest_interval = models.IntegerField(default=60)
    weight = models.IntegerField(default=0)
    reps = models.IntegerField(default=1)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
