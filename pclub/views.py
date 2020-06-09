from django.shortcuts import render
from django.http import HttpResponse
from .models import HomepageImages
import os
# Create your views here.
from django.template import context


def get_homepage(request):
    # # path = "..\PClub_Contest\pclub\static\images"
    # # img_list = os.listdir(path)
    img_list = HomepageImages.objects.all()
    #
    return render(request, 'pclub/index.html',context = {"img_list": img_list})


def mail(request):
    return render(request, 'pclub/mail.php')
