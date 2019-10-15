from django.shortcuts import render

# Create your views here.
def index(request):
    # info = Info.objects.all()
    # l=len(info)
    # context = {
    #     'info' : info,
    #     'length' : l
    # }
    return render(request, 'home/index.html')