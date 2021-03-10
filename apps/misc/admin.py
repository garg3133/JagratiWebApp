from django.contrib import admin
from django import forms
from .models import Initiative

# Register your models here

class InitiativeAdminForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = ['title', 'description', 'thumb_url', 'thumbnail']

    def clean(self):
        cleaned_data = self.cleaned_data
        thumb_url = cleaned_data.get('thumb_url')
        thumbnail = cleaned_data.get('thumbnail')
        if not thumbnail and not thumb_url:
            raise forms.ValidationError(
                "Both thumbnail and thumb_url cannot be empty.")
        return cleaned_data


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    form = InitiativeAdminForm
