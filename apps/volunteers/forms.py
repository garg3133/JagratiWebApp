from django import forms

from home.models import Schedule
from .models import VolunteerSchedule


class VolunteerScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = VolunteerSchedule
        fields = ['volun', 'day', 'schedule']

    def clean(self):
        cleaned_data = self.cleaned_data
        schedule = cleaned_data.get('schedule')
        cleaned_data['day'] = Schedule.objects.get(id=schedule.id).day
        return cleaned_data
