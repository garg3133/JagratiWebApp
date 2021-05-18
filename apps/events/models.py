from django.conf import settings
from django.db import models

from apps.volunteers.models import Volunteer
from apps.students.models import Student


def event_thumbmail_path(instance, filename):
    return f'events/{instance.id}/thumbnail/{filename}'


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2500)
    schedule = models.DateTimeField()
    venue = models.CharField(max_length=50)
    thumbnail = models.ImageField(
        upload_to='<event>.get_thumbnail_url', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return settings.STATIC_URL + 'home/images/02.jpg'

class Team(models.Model):
    team_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Management(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


class Participant(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


def event_gallery_path(instance, filename):
    return f'events/{instance.id}/{filename}'


class Gallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=event_gallery_path)
    # Whether to display the image on Captures Page or not
    capture = models.BooleanField(default=False)

    def __str__(self):
        return f's{self.id}'
