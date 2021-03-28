from django.contrib import admin

from .forms import InitiativeAdminForm
from .models import Initiative


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    form = InitiativeAdminForm

    list_display = ('title',)
