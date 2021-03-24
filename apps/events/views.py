from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Hello World!')


def add_event(request):
    return HttpResponse('Add events page..')
