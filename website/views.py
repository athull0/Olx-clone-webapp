from django.shortcuts import render
from user.models import *


# Create your views here.


def homepage(request):
    if request.user.is_authenticated:

        ads = Ad.objects.exclude(user=request.user)
    else:
        ads = Ad.objects.all()
        
    return render(request,'home.html',{'ads':ads})

