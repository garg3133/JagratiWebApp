from django.contrib import admin

from .models import (
    Designation, Volunteer, VolunteerSchedule,
    VolunteerAttendence, UpdateScheduleRequest,
)

# Register your models here.

class VolunteerInline(admin.StackedInline):
    model = Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'get_name', 'desig', 'get_auth')
    search_fields = ('roll_no', 'profile__first_name', 'profile__last_name')
    list_filter = ('desig', 'profile__user__auth')
    ordering = ('-profile__user__date_joined',)

    def get_name(self, obj):
        return f'{obj.profile.get_full_name}'
    get_name.short_description = 'Name'

    def get_auth(self, obj):
        return obj.profile.user.auth
    get_auth.short_description = 'Auth'
    get_auth.admin_order_field = 'profile__user__auth'
    get_auth.boolean = True

