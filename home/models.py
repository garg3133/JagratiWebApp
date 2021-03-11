import calendar
from django.db import models


class Calendar(models.Model):
    date = models.DateField(primary_key=True)
    remark = models.TextField(max_length=255, blank=True)
    class_scheduled = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Calendar'

    def __str__(self):
        return str(self.date)


class Section(models.Model):
    section_id = models.CharField(
        max_length=5, unique=True)   # For grouping and sorting
    name = models.CharField(max_length=30, unique=True)
    is_parent_section = models.BooleanField(default=False)
    parent_section = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'is_parent_section': True})

    def __str__(self):
        return self.name


class Schedule(models.Model):
    # They won't ever change and will give us dropdown in Admin site
    DAY = [(i+1, calendar.day_name[i]) for i in range(0, 7)]

    SUBJECT = (
        ('eng', "English"),
        ('hin', "Hindi"),
        ('mat', "Mathematics"),
        ('sci', "Science"),
        ('mab', "Mental Ability"),
    )

    sub_dict = dict(SUBJECT)

    day = models.IntegerField(choices=DAY)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.CharField(max_length=3, choices=SUBJECT)

    def get_subject(self):
        return self.sub_dict[self.subject]

    class Meta:
        unique_together = (('day', 'section'),)

    def __str__(self):
        return f'{self.get_day_display()} - {self.section.name} - {self.sub_dict[self.subject]}'


class ClassworkHomework(models.Model):
    cal_date = models.ForeignKey(Calendar, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    to_be_taught = models.TextField(
        max_length=1023, blank=True)  # Content to be taught
    subject_taught = models.CharField(max_length=3, choices=Schedule.SUBJECT)
    cw = models.TextField(max_length=1023, blank=True)
    hw = models.TextField(max_length=1023, blank=True)
    comment = models.TextField(max_length=1023, blank=True)

    class Meta:
        unique_together = (('cal_date', 'section'),)
        verbose_name = 'ClassWork/HomeWork'
        verbose_name_plural = 'ClassWork/HomeWork'

    def __str__(self):
        return f'{self.cal_date} - {self.section.name}'
