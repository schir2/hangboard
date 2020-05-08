from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from main.managers import SimpleModelManager
from main.managers import WorkoutManager
from django.utils import timezone


class SimpleModel(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    custom = models.BooleanField(default=True)
    climber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = SimpleModelManager()

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
    LEFT = 'L'
    MIDDLE = 'M'
    RIGHT = 'R'
    POSITIONS = ((LEFT, 'left'), (MIDDLE, 'middle'), (RIGHT, 'right'),)
    hangboard = models.ForeignKey(Hangboard, on_delete=models.CASCADE)
    hold_type = models.ForeignKey(HoldType, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(default=20, null=True, blank=True)
    angle = models.IntegerField(null=True, blank=True)
    max_fingers = models.IntegerField(default=4)
    position_id = models.PositiveIntegerField(default=1)
    position = models.CharField(max_length=32, choices=POSITIONS, default=MIDDLE)

    class Meta:
        pass
        unique_together = (('position_id', 'hangboard',),)

    def is_same_type(self, other) -> bool:
        return all((self.hold_type_id == other.hold_type_id, self.max_fingers == other.max_fingers, self.size == other.size,
                    self.angle == other.angle,))


class BaseWorkout(SimpleModel):
    slug = models.SlugField(unique=True)
    note = models.TextField(blank=True, null=True, default='')
    completed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Workout(BaseWorkout):
    hangboard = models.ForeignKey(Hangboard, on_delete=models.CASCADE)
    logged = models.DateTimeField(auto_now_add=True)
    difficulty = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    objects = WorkoutManager()

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
    position = models.PositiveIntegerField(default=1)
    custom = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    logged = models.DateTimeField(default=timezone.now)

    # Foreign keys
    climber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

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

    def __str__(self):
        string_builder = [self.exercise.name, self.position]
        left_hold = Hold.objects.get(pk=self.left_hold.pk) if self.left_hold else None
        right_hold = Hold.objects.get(pk=self.right_hold.pk) if self.right_hold else None
        if self.left_hold and self.right_hold:
            # Getting Hold Objects
            if all([self.left_fingers == self.right_fingers, left_hold.is_same_type(right_hold)]):
                string_builder.append(self.left_hold.size)
                string_builder.append(self.left_hold.hold_type.name)
                string_builder.append(f'Fingers {self.left_fingers}')
            else:
                string_builder.append(self.left_hold.name)
                string_builder.append(f'Fingers {self.left_fingers}')
                string_builder.append(self.right_hold.name)
                string_builder.append(f'Fingers {self.right_fingers}')
        elif self.left_hold:
            string_builder.append(self.left_hold.name)
            string_builder.append(self.left_fingers)
        elif self.right_hold:
            string_builder.append(self.right_hold.name)
            string_builder.append(f'Fingers {self.right_fingers}')
        else:
            raise ValueError('No Holds Selected')

        string_builder.append(f'Duration {self.duration}')
        string_builder.append(f'Reps {self.reps}')

        return ' | '.join(str(string_) for string_ in string_builder if string_)


class WorkoutSet(BaseWorkoutSet):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    left_hold = models.ForeignKey(Hold, related_name='workout_set_left_hold', on_delete=models.CASCADE)
    right_hold = models.ForeignKey(Hold, related_name='workout_set_right_hold', on_delete=models.CASCADE)


class TemplateWorkoutSet(BaseWorkoutSet):
    workout = models.ForeignKey(TemplateWorkout, on_delete=models.CASCADE)
    left_hold = models.ForeignKey(Hold, related_name='template_workout_set_left_hold', on_delete=models.CASCADE)
    right_hold = models.ForeignKey(Hold, related_name='template_workout_set_right_hold', on_delete=models.CASCADE)
