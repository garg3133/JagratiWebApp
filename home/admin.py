from django.contrib import admin

from .models import Calendar, ClassworkHomework, Schedule, Section

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'class_scheduled', 'remark')
    search_fields = ('date',)
    list_filter = ('class_scheduled',)
    ordering = ('-date',)

@admin.register(ClassworkHomework)
class ClassworkHomeworkAdmin(admin.ModelAdmin):
    list_display = ('cal_date', 'section', 'subject_taught')
    search_fields = ('cal_date',)
    list_filter = ('subject_taught', 'section__name',)
    ordering = ('-cal_date__date', 'section__section_id')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'section', 'subject')
    list_filter = ('day', 'subject', 'section__name')
    ordering = ('day', 'section__section_id')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'name')
    search_fields = ('name',)
    ordering = ('section_id',)
