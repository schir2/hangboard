from django.contrib import admin

from climbers.models import Climber
from climbers.models import Profile
from climbers.models import Preference
from climbers.models import Height
from climbers.models import Weight


class AutoAddClimberModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.account = request.user
        super().save_model(request, obj, form, change)


@admin.register(Climber)
class ClimberAdmin(AutoAddClimberModelAdmin):
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
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    pass


class StatAdmin(AutoAddClimberModelAdmin):
    fields = (
        'logged',
        'edited',
        'climber',
        'created',
    )

    readonly_fields = (
        'edited',
        'created',
    )

@admin.register(Height)
class HeightAdmin(StatAdmin):
    fields = ('height',) + StatAdmin.fields


@admin.register(Weight)
class WeightAdmin(StatAdmin):
    fields = ('weight',) + StatAdmin.fields
