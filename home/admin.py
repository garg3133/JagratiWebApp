from django.contrib import admin
from .models import (
	Calendar, ClassworkHomework, Designation, Feedback,
	Schedule, Section, Student, StudentAttendence,
	StudentSchedule, UpdateScheduleRequest, Volunteer,
	VolunteerAttendence, VolunteerSchedule,
)
# Register your models here.

admin.site.register(Designation)

@admin.register(Volunteer)
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


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ( 'get_name', 'school_class', 'village')
	search_fields = ('first_name', 'last_name')
	list_filter = ('school_class', 'village')
	ordering = ('school_class', 'first_name')

	def get_name(self, obj):
		return obj.first_name + ' ' + obj.last_name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'first_name'


admin.site.register(Section)
admin.site.register(Schedule)

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
	list_display = ('date', 'class_scheduled', 'remark')
	search_fields = ('date',)
	list_filter = ('class_scheduled',)
	ordering = ('date',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'date')
	ordering = ('-date',)


@admin.register(UpdateScheduleRequest)
class UpdateScheduleRequestAdmin(admin.ModelAdmin):
	list_display = ('volunteer', 'get_name', 'date', 'approved', 'declined', 'by_admin', 'cancelled')
	search_fields = ('volunteer__roll_no', 'volunteer__first_name', 'volunteer__last_name')
	list_filter = ('approved', 'declined', 'by_admin', 'cancelled')
	ordering = ('-date',)

	def get_name(self, obj):
		return obj.volunteer.first_name + ' ' + obj.volunteer.last_name
	get_name.short_description = 'Name'


@admin.register(VolunteerSchedule)
class VolunteerScheduleAdmin(admin.ModelAdmin):
	list_display = ('get_roll', 'get_name', 'day', 'get_section')
	search_fields = ('roll_no__roll_no', 'roll_no__first_name', 'roll_no__last_name')
	list_filter = ('day',)
	ordering = ('roll_no__roll_no',)

	def get_roll(self, obj):
		return obj.roll_no.roll_no
	get_roll.short_description = 'Roll No.'
	get_roll.admin_order_field = 'roll_no__roll_no'

	def get_name(self, obj):
		return obj.roll_no.first_name + ' ' + obj.roll_no.last_name
	get_name.short_description = 'Name'

	def get_section(self, obj):
		return obj.schedule.section.name
	get_section.short_description = 'Section'


admin.site.register(StudentSchedule)
admin.site.register(ClassworkHomework)
admin.site.register(VolunteerAttendence)

@admin.register(StudentAttendence)
class StudentAttendenceAdmin(admin.ModelAdmin):
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
