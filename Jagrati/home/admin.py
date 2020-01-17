from django.contrib import admin
from . import models
# Register your models here.

class VolunteerAdmin(admin.ModelAdmin):
	list_display = ('roll_no', 'get_name', 'get_auth')
	search_fields = ('roll_no', 'first_name', 'last_name')
	list_filter = ('desig', 'email__auth')
	ordering = ('-email__date_joined',)

	def get_name(self, obj):
		return obj.first_name + ' ' + obj.last_name
	get_name.short_description = 'Name'

	def get_auth(self, obj):
		return obj.email.auth
	get_auth.short_description = 'Auth'
	get_auth.admin_order_field = 'email__auth'
	get_auth.boolean = True

admin.site.register(models.Volunteer, VolunteerAdmin)

class StudentAdmin(admin.ModelAdmin):
	list_display = ( 'get_name', 'school_class', 'village')
	search_fields = ('first_name', 'last_name')
	list_filter = ('school_class', 'village')
	ordering = ('school_class', 'first_name')

	def get_name(self, obj):
		return obj.first_name + ' ' + obj.last_name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'first_name'

admin.site.register(models.Student, StudentAdmin)

admin.site.register(models.Schedule)

class CalendarAdmin(admin.ModelAdmin):
	list_display = ('date', 'class_scheduled', 'remark')
	search_fields = ('date',)
	list_filter = ('class_scheduled',)
	ordering = ('date',)

admin.site.register(models.Calendar, CalendarAdmin)

class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'date')
	ordering = ('-date',)

admin.site.register(models.Feedback, FeedbackAdmin)

class UpdateScheduleRequestAdmin(admin.ModelAdmin):
	list_display = ('volunteer', 'get_name', 'date', 'approved', 'declined', 'by_admin', 'cancelled')
	search_fields = ('volunteer__roll_no', 'volunteer__first_name', 'volunteer__last_name')
	list_filter = ('approved', 'declined', 'by_admin', 'cancelled')
	ordering = ('-date',)

	def get_name(self, obj):
		return obj.volunteer.first_name + ' ' + obj.volunteer.last_name
	get_name.short_description = 'Name'

admin.site.register(models.UpdateScheduleRequest, UpdateScheduleRequestAdmin)

admin.site.register(models.Volunteer_schedule)
admin.site.register(models.Student_schedule)
admin.site.register(models.Cw_hw)
admin.site.register(models.Volunteer_attended_on)

class StudentAttendedOnAdmin(admin.ModelAdmin):
	list_display = ('date', 'get_name', 'get_class', 'present')
	search_fields = ('date', 'sid__first_name', 'sid__last_name')
	list_filter = ('present', 'sid__school_class', 'sid__village')
	ordering = ('-date', 'sid__school_class', 'sid__first_name')

	def get_name(self, obj):
		return obj.sid.first_name + ' ' + obj.sid.last_name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'first_name'

	def get_class(self, obj):
		return obj.sid.school_class
	get_class.short_description = 'Class'
	get_class.admin_order_field = 'sid__school_class'

admin.site.register(models.Student_attended_on, StudentAttendedOnAdmin)