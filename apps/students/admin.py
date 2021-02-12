from django.contrib import admin

from .models import (
    Student,
    StudentAttendance,
    StudentSchedule,
)

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("get_name", "school_class", "village")
    search_fields = ("first_name", "last_name")
    list_filter = ("school_class", "village")
    ordering = ("school_class", "first_name")

    def get_name(self, obj):
        return obj.get_full_name

    get_name.short_description = "Name"
    get_name.admin_order_field = "first_name"


@admin.register(StudentSchedule)
class StudentScheduleAdmin(admin.ModelAdmin):
    list_display = ("get_class", "get_name", "day", "get_section")
    search_fields = ("student__first_name", "student__last_name")
    list_filter = ("day", "student__school_class", "schedule__section__name")
    ordering = ("student__school_class", "student__first_name", "day")

    def get_class(self, obj):
        return obj.student.school_class

    get_class.short_description = "Class"
    get_class.admin_order_field = "student__school_class"

    def get_name(self, obj):
        return obj.student.get_full_name

    get_name.short_description = "Name"
    get_name.admin_order_field = "student__first_name"

    def get_section(self, obj):
        return obj.schedule.section.name

    get_section.short_description = "Section"
    get_section.admin_order_field = "schedule__section__section_id"


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "cal_date",
        "get_name",
        "get_class",
        "get_village",
        "present",
        "hw_done",
    )
    search_fields = ("cal_date", "student__first_name", "student__last_name")
    list_filter = ("present", "student__school_class",
                   "student__village", "hw_done")
    ordering = ("-cal_date", "student__school_class", "student__first_name")

    def get_name(self, obj):
        return obj.student.get_full_name

    get_name.short_description = "Name"
    get_name.admin_order_field = "student__first_name"

    def get_class(self, obj):
        return obj.student.school_class

    get_class.short_description = "Class"
    get_class.admin_order_field = "student__school_class"

    def get_village(self, obj):
        return obj.student.get_village_display()

    get_village.short_description = "Village"
    get_village.admin_order_field = "student__village"
