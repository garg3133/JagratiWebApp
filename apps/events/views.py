from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Event
from django.contrib import message


def index(request):
    return HttpResponse('Hello World!')


@permission_required('events.add_event', raise_exception=True)
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        schedule = request.POST.get('schedule')
        venue = request.POST['venue']
        description = request.POST['description']
        thumbnail = request.FILES.get('thumbnail')

        event = Event(
            title=title, schedule=schedule, venue=venue, description=description, thumbnail=thumbnail,
        )
        event.save()

        messages.success(request, "Event added successfully!")
        return redirect('events:add_event')

    return render(request, 'events/add_event.html')
