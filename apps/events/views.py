from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, user_passes_test, permission_required
)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from home.views import has_authenticated_profile
from .models import Event


def index(request):
    return HttpResponse('Hello World!')


def captures(request):
    return render(request, 'events/captures.html')


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permission_required('events.add_event', raise_exception=True)
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        schedule = request.POST['schedule']
        venue = request.POST['venue']
        thumbnail = request.FILES.get('thumbnail')

        event = Event(
            title=title, schedule=schedule, venue=venue,
            description=description, thumbnail=thumbnail,
        )
        event.save()

        messages.success(request, "Event added successfully!")
        return redirect('events:add_event')

    return render(request, 'events/add_event.html')
    