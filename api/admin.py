from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Device, Box, Schedule, Alert, UserAlert, DeviceToken, User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    filter_horizontal = BaseUserAdmin.filter_horizontal + ('devices',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Devices', {'fields': ('devices',)}),
    )

admin.site.register(Device)
admin.site.register(Box)
admin.site.register(Schedule)
admin.site.register(Alert)
admin.site.register(UserAlert)
admin.site.register(DeviceToken)