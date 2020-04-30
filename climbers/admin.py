from django.contrib import admin

from climbers.models import Climber


@admin.register(Climber)
class AccountAdmin(admin.ModelAdmin):
    fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_display = fields
