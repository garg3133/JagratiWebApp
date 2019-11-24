from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Volunteer)
admin.site.register(models.Student)
admin.site.register(models.Schedule)

class CalendarAdmin(admin.ModelAdmin):
	list_display = ('date', 'class_scheduled', 'remark')
	search_fields = ('date',)
	list_filter = ('class_scheduled',)
	ordering = ('date',)


admin.site.register(models.Calendar, CalendarAdmin)
admin.site.register(models.Volunteer_schedule)
admin.site.register(models.Student_schedule)
admin.site.register(models.Cw_hw)
admin.site.register(models.Volunteer_attended_on)
admin.site.register(models.Student_attended_on)