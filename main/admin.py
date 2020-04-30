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


class AutoAddAccountModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.account = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        abstract = True


class SimpleModelAdmin(AutoAddAccountModelAdmin):
    list_display = ('name', 'slug', 'description', 'created', 'updated', 'account')
    fields = ('name', 'slug', 'description', 'account')

    class Meta:
        abstract = True


@admin.register(Hold)
class HoldAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'slug',
        'hold_type',
        'hangboard',
        'description',
        'created',
        'updated',
        'account'
    )
    fields = (
        'name',
        'slug',
        'hold_type',
        'hangboard',
        'description',
        'account'
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
class HangboardAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'slug',
        'material',
        'description',
        'created',
        'updated',
        'account',
    )
    fields = (
        'name',
        'slug',
        'material',
        'description',
        'account',
    )


@admin.register(WorkoutSet)
class WorkoutSetAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'exercise',
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_interval',
        'duration',
        'weight',
        'reps',
        'account',
    )
    fields = (
        'name',
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_interval',
        'duration',
        'weight',
        'reps',
        'exercise',
        'account',
    )


@admin.register(Workout)
class WorkoutAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'slug',
        'description',
        'created',
        'updated',
        'scheduled',
        'completed',
        'account',
    )
    fields = (
        'name',
        'slug',
        'description',
        'created',
        'updated',
        'scheduled',
        'completed',
        'account',
    )


@admin.register(TemplateWorkout)
class TemplateWorkoutAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'slug',
        'description',
        'created',
        'updated',
        'account',
    )

@admin.register(TemplateWorkoutSet)
class TemplateWorkoutSetAdmin(AutoAddAccountModelAdmin):
    list_display = (
        'name',
        'exercise',
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_interval',
        'duration',
        'weight',
        'reps',
        'account',
    )
    fields = (
        'name',
        'workout',
        'left_hold',
        'left_fingers',
        'right_hold',
        'right_fingers',
        'rest_interval',
        'duration',
        'weight',
        'reps',
        'exercise',
        'account',
    )