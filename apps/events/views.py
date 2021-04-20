from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, user_passes_test, permission_required
)
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from home.views import has_authenticated_profile
from .models import Event, Gallery
from math import ceil


def index(request):
    events = Event.objects.all()
    print(events)
    n = len(events)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'event': events}
    
    return render(request,'events/index.html',params)


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


def show_event(request,myid):
    all_event=[]
    event = Event.objects.filter(id=myid)
    
    all_image=Gallery.objects.filter(id=myid)
    all_title=Gallery.objects.values('event','id','capture')
    tit = {item['event'] for item in all_title }
    print(all_title)
    for t in tit:
        print("T: ",t)
      #  print("selected id: ",)
        event_list = Gallery.objects.filter(event_id=t)
        n = len(event_list)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if t==myid:
            all_event.append([event_list, range(1, nSlides), nSlides])
            break
        print(event_list)
    params = {'my_event':event[0],'all_events': all_event}
    return render(request, 'events/show_event.html',params)
