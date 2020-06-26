from django.core.mail import BadHeaderError
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .forms import ContactForm, NewsletterForm
from .models import HomepageImages
from .models import Events, EventGallery, Resources
from .models import Teams, Newsletter
from datetime import date, timedelta
from django.db.models import Q
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_homepage(request):
    img_list = HomepageImages.objects.all()
    core = Teams.objects.filter(committee_type='Core Committee')
    exec = Teams.objects.filter(committee_type='Executive Committee')
    event_name = EventGallery.objects.values('event_name').distinct()
    upcoming_events = Events.objects.filter(Q(event_date__gt=date.today()) | Q(event_date=date.today()))
    enddate = date.today()
    startdate = enddate - timedelta(days=2)
    res = Resources.objects.filter(created_date__range=[startdate, enddate])

    images = []
    for i in event_name:
        img = (EventGallery.objects.filter(event_name=i.get('event_name')))
        if len(img) != 0:
            images.append(img)

    if request.method == 'GET':
        form = ContactForm()
    else:
        print(request.POST)
        form = ContactForm(request.POST)
        print(form)
        if form.is_valid():
            receiver_address = 'nancy.r@ahduni.edu.in'
            subject = form.cleaned_data['Subject']
            sender_pass = '9824228740'
            sender_address = 'nancy.r@ahduni.edu.in'
            mail_content = form.cleaned_data['Message']
            print(subject)
            print(subject == None)
            try:
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = subject
                message.attach(MIMEText(mail_content, 'plain'))
                session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                session.starttls()  # enable security
                session.login(sender_address, sender_pass)  # login with mail_id and password
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()
                print('Mail Sent')

            except BadHeaderError:
                print(BadHeaderError)
                return HttpResponse('Invalid header found.')

    form1 = NewsletterForm(request.POST or None)
    if form1.is_valid():
        form1.save()

    emaillist = Newsletter.objects.all().values_list('email')
    print(emaillist)
    return render(request, 'pclub/index.html',
                  context={"img_list": img_list, "core": core, "exec": exec, "upcoming_events": upcoming_events,
                           "images": images, "res": res, "form": form, "form1": form1})


def get_events(request):
    team = Teams.objects.order_by('designation')
    events = Events.objects.all()
    eventimages = EventGallery.objects.all()

    past_events = Events.objects.filter(Q(event_date__lt=date.today()))
    upcoming_events = Events.objects.filter(Q(event_date__gt=date.today()) | Q(event_date=date.today()))
    event_name = EventGallery.objects.values('event_name').distinct()
    images = []
    for i in event_name:
        img = (EventGallery.objects.filter(event_name=i.get('event_name')))

        if len(img) != 0:
            images.append(img)

    return render(request, 'pclub/events.html',
                  context={"past_events": past_events, "upcoming_events": upcoming_events, "team": team,
                           "images": images, "eventimages": eventimages})


def get_resources(request):
    tags = Resources.objects.values('tag').distinct()
    resource = []
    for i in tags:
        res = (Resources.objects.filter(tag=i.get('tag')))
        if len(res) != 0:
            resource.append(res)
    return render(request, 'pclub/resources.html', context={"resource": resource})


def setcookie(request):
    html = HttpResponse("<h1>Dataflair Django Tutorial</h1>")
    html.set_cookie('dataflair', 'Hello this is your Cookies', max_age=None)
    return html
