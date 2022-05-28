from django.conf import settings
from django.db import models

from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from home.models import Calendar, Schedule


class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    VILLAGE = (
        ('G', 'Gadheri'),
        ('M', 'Mehgawan'),
        ('C', 'Chanditola'),
        ('A', 'Amanala'),
        ('S', 'Suarkol'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    profile_image = ProcessedImageField(
        upload_to='students/profile_pics', processors=[ResizeToFill(300, 300)],
        format='JPEG', options={'quality': 60}, blank=True)
    school_class = models.IntegerField()
    village = models.CharField(max_length=3, choices=VILLAGE)
    contact_no = models.CharField(max_length=13, blank=True)
    guardian_name = models.CharField(max_length=30)

    restricted = models.BooleanField(default=False)
    verified = models.BooleanField(verbose_name='Profile details verified', default=False)
    remarks = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f'{self.get_full_name} ({self.school_class})'

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def has_complete_profile(self):
        if (self.first_name != '.' and self.last_name != '.' and '.' not in self.guardian_name
            and self.contact_no and self.profile_image):
            return True
        return False

    @property
    def get_verified_name(self):
        sign = ''
        if not self.has_complete_profile:
            sign = '&#10071; '
        elif not self.verified:
            sign = '&#10008; '
        else:
            sign = '&#10004; '
        return f'{sign}{self.first_name} {self.last_name}'

    @property
    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        elif self.gender == 'F':
            return settings.STATIC_URL + 'home/images/woman.png'
        else:
            return settings.STATIC_URL + 'home/images/man.png'

    @property
    def profile_url(self):
        """Returns the url to student profile."""
        return reverse('students:profile', args=[str(self.id)])


class StudentSchedule(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_schedules')
    day = models.IntegerField(choices=Schedule.DAY, blank=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='student_schedules')

    class Meta:
        unique_together = (('student', 'day'),)
        verbose_name = 'Student Schedule'
        verbose_name_plural = 'Students Schedule'

    def __str__(self):
        return f'{self.student} - {self.schedule}'


class StudentAttendance(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_attendance')
    cal_date = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, related_name='student_attendance')
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
