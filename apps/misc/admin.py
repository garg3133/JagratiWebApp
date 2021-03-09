from django.contrib import admin

# Register your models here.
from .models import Initiative

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title',)
