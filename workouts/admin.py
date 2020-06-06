from django.contrib import admin

from workouts.models import Hold
from workouts.models import Hangboard
from workouts.models import HoldType
from workouts.models import Workout
from workouts.models import WorkoutSet
from workouts.models import Exercise
from workouts.models import TemplateWorkout
from workouts.models import TemplateWorkoutSet


class AutoAddClimberModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.climber = request.user
        super().save_model(request, obj, form, change)


class SimpleModelAdmin(AutoAddClimberModelAdmin):
    list_display = (
        'name',
        'description',
        'climber',
    )
    fields = (
        'name',
        'slug',
        'description',
        'climber',
    )


@admin.register(Hold)
class HoldAdmin(AutoAddClimberModelAdmin):
    list_display = (
        'name',
        'hold_type',
        'max_fingers',
        'size',
        'angle',
        'hangboard',
        'position_id',
        'description',
        'climber'
    )
    fields = (
        'name',
        'hold_type',
        'max_fingers',
        'size',
        'angle',
        'hangboard',
        'position_id',
        'description',
        'climber',
    )


@admin.register(Exercise)
class ExerciseAdmin(SimpleModelAdmin):
    pass


@admin.register(HoldType)
class HoldTypeAdmin(SimpleModelAdmin):
    pass


@admin.register(Hangboard)
class HangboardAdmin(AutoAddClimberModelAdmin):

    list_display = (
        'name',
        'image',
        'description',
        'climber',
    )
    fields = (
        'pk',
        'name',
        'image',
        'description',
        'climber',
    )
    readonly_fields = ('pk',)


class BaseWorkoutSetAdmin(AutoAddClimberModelAdmin):
    list_display = (
        'pk',
        'previous_id',
        'exercise',
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_between',
        'duration',
        'weight',
        'reps',
        'climber',
    )
    fields = (
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_between',
        'duration',
        'weight',
        'reps',
        'exercise',
        'updated',
        'logged',
        'climber',
        'previous',
    )


@admin.register(WorkoutSet)
class WorkoutSetAdmin(BaseWorkoutSetAdmin):
    pass


@admin.register(TemplateWorkoutSet)
class TemplateWorkoutSetAdmin(BaseWorkoutSetAdmin):
    pass


class BaseWorkoutAdmin(AutoAddClimberModelAdmin):
    list_display = (
        'name',
        'description',
        'created',
        'updated',
        'completed',
        'climber',
    )
    fields = (
        'name',
        'hangboard',
        'description',
        'completed',
        'climber',
        'logged',
    )


@admin.register(Workout)
class WorkoutAdmin(BaseWorkoutAdmin):
    pass


@admin.register(TemplateWorkout)
class TemplateWorkoutAdmin(BaseWorkoutAdmin):
    pass
