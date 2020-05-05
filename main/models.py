from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class SimpleModel(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    custom = models.BooleanField(default=True)
    climber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'name={self.name},' \
               f'slug={self.slug},' \
               f'custom={self.custom},' \
               f'climber={self.climber},' \
               f'created={self.created},' \
               f'updated={self.updated}'

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
    size = models.PositiveIntegerField(default=20, null=True, blank=True)
    angle = models.IntegerField(null=True, blank=True)
    max_fingers = models.IntegerField(default=4)
    position = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('position', 'hangboard',),)


class BaseWorkout(SimpleModel):
    note = models.TextField(blank=True, null=True, default='')
    completed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Workout(BaseWorkout):
    hangboard = models.ForeignKey(Hangboard, on_delete=models.CASCADE)
    scheduled = models.DateTimeField(auto_now_add=True)
    difficulty = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        get_latest_by = ('updated',)


class TemplateWorkout(BaseWorkout):
    pass


class BaseWorkoutSet(models.Model):

    # Not Implemented
    left_hold = NotImplemented
    right_hold = NotImplemented

    # Simple Fields
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    left_fingers = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(5)])
    right_fingers = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(5)])
    rest_between = models.PositiveIntegerField(default=60)
    rest_after = models.PositiveIntegerField(default=60)
    duration = models.PositiveIntegerField(default=0)
    weight = models.IntegerField(default=0)
    reps = models.PositiveIntegerField(default=1)
    position = models.PositiveIntegerField(default=0)
    custom = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Foreign keys
    climber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True
        unique_together = (('position', 'workout'),)
        get_latest_by = ('position',)

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'climber={self.climber},' \
               f'exercise={self.exercise},' \
               f'left_hold={self.left_hold},' \
               f'left_fingers={self.left_fingers},' \
               f'right_hold={self.right_hold},' \
               f'right_fingers={self.right_fingers},' \
               f'rest_between={self.rest_between},' \
               f'rest_after={self.rest_after},' \
               f'duration={self.duration},' \
               f'weight={self.weight},' \
               f'reps={self.reps},' \
               f'position={self.position},' \
               f'custom={self.custom},' \
               f'completed={self.completed},' \
               f'created={self.created},' \
               f'updated={self.updated})'


class WorkoutSet(BaseWorkoutSet):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    left_hold = models.ForeignKey(Hold, related_name='workout_set_left_hold', on_delete=models.CASCADE, null=True, blank=True)
    right_hold = models.ForeignKey(Hold, related_name='workout_set_right_hold', on_delete=models.CASCADE, null=True, blank=True)


class TemplateWorkoutSet(BaseWorkoutSet):
    workout = models.ForeignKey(TemplateWorkout, on_delete=models.CASCADE)
    left_hold = models.ForeignKey(Hold, related_name='template_workout_set_left_hold', on_delete=models.CASCADE, null=True, blank=True)
    right_hold = models.ForeignKey(Hold, related_name='template_workout_set_right_hold', on_delete=models.CASCADE, null=True, blank=True)