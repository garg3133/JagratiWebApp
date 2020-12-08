from django.db import models

from home.models import Calendar, Schedule

# Create your models here.

class Student(models.Model):
    VILLAGE = (
        ('G', 'Gadheri'),
        ('M', 'Mehgawan'),
        ('C', 'Chanditola'),
        ('A', 'Amanala'),
        ('S', 'Suarkol'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school_class = models.IntegerField()
    village = models.CharField(max_length=3, choices=VILLAGE)
    contact_no = models.CharField(max_length=13, blank=True)
    guardian_name = models.CharField(max_length=30, blank=True)
    restricted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_full_name} ({self.school_class})'

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class StudentSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_schedules')
    day = models.IntegerField(choices=Schedule.DAY, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='student_schedules')

    class Meta:
        unique_together = (('student', 'day'),)
        verbose_name = 'Student Schedule'
        verbose_name_plural = 'Students Schedule'

    def __str__(self):
        return f'{self.student} - {self.schedule}'

    def save(self, *args, **kwargs):
        self.day = Schedule.objects.get(id=self.schedule.id).day
        super(StudentSchedule, self).save(*args, **kwargs)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_Attendance')
    cal_date = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='student_Attendance')
    present = models.BooleanField(default=False)
    hw_done = models.BooleanField(default=False, verbose_name="HomeWork Done")

    class Meta:
        unique_together = (('student', 'cal_date'),)
        verbose_name = 'Student Attendance'
        verbose_name_plural = 'Students Attendance'

    def __str__(self):
        return f'{self.student} - {self.cal_date}'

    def save(self, *args, **kwargs):
        """For cpanel."""
        self.present = (self.present is True)
        self.hw_done = (self.hw_done is True)
        super(StudentAttendance, self).save(*args, **kwargs)
