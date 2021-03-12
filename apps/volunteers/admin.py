from django.contrib import admin

from .forms import VolunteerScheduleAdminForm
from .models import (
    Designation, Volunteer, VolunteerSchedule,
    VolunteerAttendance, UpdateScheduleRequest,
)


class VolunteerInline(admin.StackedInline):
    model = Volunteer


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('desig_id', 'name', 'parent_desig')
    search_fields = ('name', 'parent_desig__name')
    list_filter = ('parent_desig',)
    ordering = ('desig_id',)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'get_name', 'desig', 'get_auth')
    search_fields = ('roll_no', 'profile__first_name', 'profile__last_name')
    list_filter = ('desig', 'profile__user__auth')
    ordering = ('-profile__user__date_joined',)

    def get_name(self, obj):
        return f'{obj.profile.get_full_name}'
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'profile__first_name'

    def get_auth(self, obj):
        return obj.profile.user.auth
    get_auth.short_description = 'Auth'
    get_auth.admin_order_field = 'profile__user__auth'
    get_auth.boolean = True


@admin.register(VolunteerSchedule)
class VolunteerScheduleAdmin(admin.ModelAdmin):
    form = VolunteerScheduleAdminForm

    list_display = ('get_roll', 'get_name', 'day', 'get_section')
    search_fields = ('volun__roll_no',
                     'volun__profile__first_name', 'volun__profile__last_name')
    list_filter = ('day',)
    ordering = ('volun__roll_no',)

    def get_roll(self, obj):
        return obj.volun.roll_no
    get_roll.short_description = 'Roll No.'
    get_roll.admin_order_field = 'volun__roll_no'

    def get_name(self, obj):
        return obj.volun.profile.get_full_name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'volun__profile__first_name'

    def get_section(self, obj):
        return obj.schedule.section.name
    get_section.short_description = 'Section'
    get_section.admin_order_field = 'schedule__section__section_id'


@admin.register(VolunteerAttendance)
class VolunteerAttendanceAdmin(admin.ModelAdmin):
    list_display = ('cal_date', 'get_roll', 'get_name', 'present', 'extra')
    search_fields = ('cal_date', 'volun__roll_no',
                     'volun__profile__first_name', 'volun__profile__last_name')
    list_filter = ('volun__batch', 'present', 'extra')
    ordering = ('-cal_date', '-volun__batch', 'volun__roll_no')

    def get_roll(self, obj):
        return obj.volun.roll_no
    get_roll.short_description = 'Roll No.'
    get_roll.admin_order_field = 'volun__roll_no'

    def get_name(self, obj):
        return obj.volun.profile.get_full_name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'volun__profile__first_name'


@admin.register(UpdateScheduleRequest)
class UpdateScheduleRequestAdmin(admin.ModelAdmin):
    list_display = ('volun', 'get_name', 'date', 'approved',
                    'declined', 'by_admin', 'cancelled')
    search_fields = ('volun__roll_no',
                     'volun__profile__first_name', 'volun__profile__last_name')
    list_filter = ('approved', 'declined', 'by_admin', 'cancelled')
    ordering = ('-date',)

    def get_name(self, obj):
        return obj.volun.profile.get_full_name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'volun__profile__first_name'
