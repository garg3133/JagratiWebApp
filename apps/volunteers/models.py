from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from accounts.models import Profile
from home.models import Calendar, Schedule

# Create your models here.
class Designation(models.Model):
    desig_id = models.CharField(max_length=10, verbose_name='Designation ID', unique=True)
    name = models.CharField(max_length=100)
    parent_desig = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Volunteer(models.Model):
    PROGRAMME = (
        ('bt', 'B.Tech'),
        ('mt', 'M.Tech'),
        ('phd', 'PhD'),
        ('bd', 'B.Des'),
        ('md', 'M.Des'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    roll_no = models.CharField(verbose_name="Roll Number", max_length=8, unique=True)
    batch = models.IntegerField()
    programme = models.CharField(max_length=3, choices=PROGRAMME)
    dob = models.DateField(verbose_name="Date of Birth")
    desig = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)  # null --> Normal Volunteer
    # resp = models.ForeignKey()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.profile.get_full_name} ({self.roll_no})'

    def save(self, *args, **kwargs):
        """For cpanel."""
        self.active = (self.active is True)
        super(Volunteer, self).save(*args, **kwargs)

@receiver(post_delete, sender=Volunteer)
def delete_related_profile(sender, instance, **kwargs):
    """Delete the related Profile."""
    instance.profile.delete()

class VolunteerSchedule(models.Model):
    volun = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='volun_schedules')
    day = models.CharField(max_length=10, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='volun_schedules')

    class Meta:
        unique_together = (('volun', 'day'),)
        verbose_name = 'Volunteer Schedule'
        verbose_name_plural = 'Volunteers Schedule'

    def __str__(self):
        return f'{self.volun} - {self.schedule}'

    def save(self, *args, **kwargs):
        self.day = Schedule.objects.get(id=self.schedule.id).day
        super(VolunteerSchedule, self).save(*args, **kwargs)

class VolunteerAttendence(models.Model):
    volun = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='volun_attendence')
    cal_date = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='volun_attendence')
    present = models.BooleanField(default=False)
    extra = models.BooleanField(default=False)

    class Meta:
        unique_together = (('volun', 'cal_date'),)
        verbose_name = 'Volunteer Attendence'
        verbose_name_plural = 'Volunteers Attendence'

    def __str__(self):
        return f'{self.volun} - {self.cal_date}'

    def save(self, *args, **kwargs):
        """For cpanel."""
        self.present = (self.present is True)
        self.extra = (self.extra is True)
        super(VolunteerAttendence, self).save(*args, **kwargs)

class UpdateScheduleRequest(models.Model):
    volun = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='update_sch_requests')
    previous_schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name='update_sch_requests_from', null=True, blank=True)
    new_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='update_sch_requests_to')
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)

    # Only one of the below booleans will be true. Request pending if all false!
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    by_admin = models.BooleanField(default=False)   # If shedule is updated by admin without request by volunteer
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.volun.__str__()

    def save(self, *args, **kwargs):
        # Create VolunteerSchedule instance
        if self.approved is True or self.by_admin is True:   # Schedule is updated in only these two cases
            prev_sch = VolunteerSchedule.objects.filter(volun=self.volun)
            if prev_sch.exists():
                prev_sch = prev_sch[0]
                prev_sch.schedule = self.updated_schedule
                prev_sch.save()
            else:
                vol_sch = VolunteerSchedule(volun=self.volun, schedule=self.updated_schedule)
                vol_sch.save()
        # For CPanel
        self.approved = (self.approved is True)
        self.declined = (self.declined is True)
        self.by_admin = (self.by_admin is True)
        self.cancelled = (self.cancelled is True)
        super(UpdateScheduleRequest, self).save(*args, **kwargs)