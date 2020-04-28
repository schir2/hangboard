from django.contrib import admin

from main.models import Hold
from main.models import Hangboard
from main.models import HoldType
from main.models import WorkoutSet
from main.models import Exercise
from main.models import Material


class SimpleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'created', 'updated', 'account')

    class Meta:
        abstract = True


@admin.register(Hold)
class HoldAdmin(SimpleModelAdmin):
    pass


@admin.register(Exercise)
class ExcerciseAdmin(SimpleModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(SimpleModelAdmin):
    pass


@admin.register(HoldType)
class HoldTypeAdmin(SimpleModelAdmin):
    pass
