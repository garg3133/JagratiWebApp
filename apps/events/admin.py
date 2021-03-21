from django.contrib import admin

from .models import Event, Team, Management, Participant, Gallery


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'schedule', 'venue')
    search_fields = ('title', 'venue')
    ordering = ('-schedule',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'name')
    search_fields = ('name',)
    ordering = ('team_id',)


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('get_event_title', 'get_team_name', 'get_volunteer_name')
    search_fields = ('event__title', 'team__name', 'volunteer__profile__first_name',
                     'volunteer__profile__last_name')
    list_filter = ('team__name',)
    ordering = ('-event__schedule', 'team__name')

    def get_event_title(self, obj):
        return obj.event.title
    get_event_title.short_description = 'Event Title'
    get_event_title.admin_order_field = 'event__title'

    def get_team_name(self, obj):
        return obj.event.title
    get_team_name.short_description = 'Team Name'
    get_team_name.admin_order_field = 'team__name'

    def get_volunteer_name(self, obj):
        return obj.volunteer.profile.get_full_name
    get_volunteer_name.short_description = 'Volunteer Name'
    get_volunteer_name.admin_order_field = 'volunteer__profile__first_name'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('get_event_title', 'get_student_name')
    search_fields = ('event__title', 'student__first_name',
                     'student__last_name')
    ordering = ('-event__schedule',)

    def get_event_title(self, obj):
        return obj.event.title
    get_event_title.short_description = 'Event Title'
    get_event_title.admin_order_field = 'event__title'

    def get_student_name(self, obj):
        return obj.student.get_full_name
    get_student_name.short_description = 'Student Name'
    get_student_name.admin_order_field = 'student__first_name'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('get_event_title', 'photo', 'capture')
    search_fields = ('event__title',)
    list_filter = ('capture',)
    ordering = ('-event__schedule',)

    def get_event_title(self, obj):
        return obj.event.title
    get_event_title.short_description = 'Event Title'
    get_event_title.admin_order_field = 'event__title'
