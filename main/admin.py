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
        'hangboard',
        'description',
        'created',
        'updated',
        'climber'
    )
    fields = (
        'name',
        'slug',
        'hold_type',
        'hangboard',
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

    def get_holds(self, request, obj):
        if obj:
            return obj.hold_set
    get_holds.short_description = 'holds'

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
        'name',
        'slug',
        'material',
        'description',
        'climber',
        'get_holds',
    )
    readonly_fields = ('get_holds',)


class BaseWorkoutSetAdmin(AutoAddClimberModelAdmin):
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
        'climber',
    )
    fields = (
        'name',
        'slug',
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
        'updated',
        'custom',
        'climber',
    )

    class Meta:
        abstract = True


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
        'slug',
        'description',
        'completed',
        'climber',
    )


@admin.register(Workout)
class WorkoutAdmin(BaseWorkoutAdmin):
    pass


@admin.register(TemplateWorkout)
class TemplateWorkoutAdmin(BaseWorkoutAdmin):
    pass
