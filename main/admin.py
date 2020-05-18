from django.contrib import admin

from main.models import Hold
from main.models import Hangboard
from main.models import HoldType
from main.models import Workout
from main.models import WorkoutSet
from main.models import Exercise
from main.models import Material
from main.models import TemplateWorkout
from main.models import TemplateWorkoutSet


class AutoAddClimberModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.climber = request.user
        super().save_model(request, obj, form, change)

    readonly_fields = (
        'updated',
        'created',
    )


class SimpleModelAdmin(AutoAddClimberModelAdmin):
    list_display = (
        'name',
        'slug',
        'description',
        'created',
        'updated',
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
        'slug',
        'hold_type',
        'max_fingers',
        'size',
        'angle',
        'hangboard',
        'position_id',
        'description',
        'created',
        'updated',
        'climber'
    )
    fields = (
        'name',
        'slug',
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


@admin.register(Material)
class MaterialAdmin(SimpleModelAdmin):
    pass


@admin.register(HoldType)
class HoldTypeAdmin(SimpleModelAdmin):
    pass


@admin.register(Hangboard)
class HangboardAdmin(AutoAddClimberModelAdmin):

    list_display = (
        'name',
        'slug',
        'material',
        'description',
        'created',
        'updated',
        'climber',
    )
    fields = (
        'pk',
        'name',
        'slug',
        'material',
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
        'slug',
        'description',
        'created',
        'updated',
        'completed',
        'climber',
    )
    fields = (
        'name',
        'hangboard',
        'slug',
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
