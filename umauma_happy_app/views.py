from django.shortcuts import render

from django.http import HttpResponse

from .models.race import Race
from django.template import loader

from datetime import datetime

# Create your views here.


def index(request):
    tdate = datetime.now()
    print(tdate)
    race_list = Race.objects.filter(date = tdate)
    context = {
        'race_list': race_list,
    }
    return render(request, 'umauma_happy_app/index.html', context)
