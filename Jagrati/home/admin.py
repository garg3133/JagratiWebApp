from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Volunteer)
admin.site.register(models.Student)
admin.site.register(models.Schedule)
admin.site.register(models.Calendar)
admin.site.register(models.Volunteer_schedule)
admin.site.register(models.Student_schedule)
admin.site.register(models.cw_hw)
admin.site.register(models.Volunteer_attended_on)
admin.site.register(models.Student_attended_on)