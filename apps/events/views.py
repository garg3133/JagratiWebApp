from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Event,Gallery
from math import ceil

def index(request):
    events = Event.objects.all()
    print(events)
    n = len(events)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'event': events}
    
    return render(request,'events/index.html',params)


def add_event(request):
    return HttpResponse('Add events page..')

def show_event(request,myid):
    all_event=[]
    event = Event.objects.filter(id=myid)
    
    all_image=Gallery.objects.filter(id=myid)
    all_title=Gallery.objects.values('event_id','id')
    tit = {item['event_id'] for item in all_title }
    
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

    