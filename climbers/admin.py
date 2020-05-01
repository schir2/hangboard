from django.contrib import admin

from climbers.models import Climber
from climbers.models import Profile
from climbers.models import Preference
from climbers.models import Measurement
from climbers.models import Height
from climbers.models import Weight


class AutoAddClimberAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.climber = request.user
        super().save_model(request, obj, form, change)


class AutoAddMeasurementAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.measurement = request.user.measurement
        super().save_model(request, obj, form, change)


@admin.register(Climber)
class ClimberAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    list_display = fields


@admin.register(Profile)
class ProfileAdmin(AutoAddClimberAdmin):
    pass


@admin.register(Preference)
class PreferenceAdmin(AutoAddClimberAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(AutoAddClimberAdmin):

    fields = ('get_current_weight', 'get_current_height',)
    readonly_fields = ('get_current_weight', 'get_current_height',)

class StatAdmin(AutoAddMeasurementAdmin):

    fields = (
        'logged',
        'edited',
        'created',
        'measurement',
    )

    readonly_fields = (
        'edited',
        'created',
        'measurement',
    )


@admin.register(Height)
class HeightAdmin(StatAdmin):
    fields = ('height',) + StatAdmin.fields


@admin.register(Weight)
class WeightAdmin(StatAdmin):
    fields = ('weight',) + StatAdmin.fields
