from django import forms

from home.models import Schedule
from .models import StudentSchedule,Student


class StudentScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = StudentSchedule
        fields = ['student', 'day', 'schedule']

    def clean(self):
        cleaned_data = self.cleaned_data
        schedule = cleaned_data.get('schedule')
        cleaned_data['day'] = Schedule.objects.get(id=schedule.id).day
        return cleaned_data

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
