from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import HomepageImages
from .models import Events
from .models import Teams
import os
# Create your views here.
from django.template import context
from django.views.generic.list import ListView


def get_homepage(request):
    # # path = "..\PClub_Contest\pclub\static\images"
    # # img_list = os.listdir(path)
    img_list = HomepageImages.objects.all()
    team = Teams.objects.order_by('designation')
    return render(request, 'pclub/index.html', context={"img_list": img_list, "team": team})


def get_events(request):
    # specify the model for list view
    events = Events.objects.all()
    # events = get_object_or_404(Events, pk=pk)
    return render(request, 'pclub/events.html', context={"events": events})
