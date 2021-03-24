from django.contrib import admin
from .models import Feedback, Contact

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('date', 'name')
    ordering = ('-date',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'email')
    ordering = ('-date',)