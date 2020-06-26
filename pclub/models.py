from __future__ import print_function
import smtplib

from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from datetime import date
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CATEGORIES = (
    ('Core Committee', 'Core Committee'),
    ('Executive Committee', 'Executive Committee'),

)


class HomepageImages(models.Model):
    class Meta:
        verbose_name_plural = 'Homepage Images'

    image = models.ImageField(upload_to='static/images/')


class Events(models.Model):
    class Meta:
        verbose_name_plural = 'Events'

    event_date = models.DateField()
    event_name = models.CharField(max_length=200)
    event_info = models.TextField()
    event_poster = models.ImageField(upload_to='static/images/', blank=True)
    event_url = models.URLField(blank=True)

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'venv/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)

        events = Events.objects.filter(Q(event_date__gt=date.today()) | Q(event_date=date.today())).values_list(
            'event_name', 'event_date')

        print(events)

        for i in events:
            date1 = i[1]
            date1 = date1.strftime("%Y-%m-%dT%H:%M:%S-00:00")
            print(date1)
            event = {
                'summary': 'Programing Club event',
                'description': i[0],
                'start': {
                    'dateTime': date1,
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': date1,
                    'timeZone': 'America/Los_Angeles',
                },

            }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        link = ('Google Calender link: %s' % (event.get('htmlLink')))

        upcoming_events = Events.objects.filter(Q(event_date__gt=date.today()) | Q(event_date=date.today()))
        if upcoming_events:
            addresslist = Newsletter.objects.all().values_list('email')
            fromaddr = 'nancy.r@ahduni.edu.in'
            for address in addresslist:
                toaddrs = address
                TEXT = 'Programming Club is coming with the new event. Go Hurry up and register the event from the website.' + link
                SUBJECT = 'Programming Club upcoming events'
                msg = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
                # Your gmail Credentials
                username = 'nancy.r@ahduni.edu.in'
                password = '9824228740'

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(username, password)
                server.sendmail(fromaddr, toaddrs, msg)
                server.quit()
                print("mail sent")
        super().save(*args, **kwargs)


class EventGallery(models.Model):
    class Meta:
        verbose_name_plural = 'Event Gallery'

    event_name = models.ForeignKey(Events, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/images/', blank=True)

    # def __str__(self):
    #     return self.event_name


class Teams(models.Model):
    class Meta:
        verbose_name_plural = 'Teams'

    committee_type = models.CharField(choices=CATEGORIES, max_length=20, default='Core Committee')
    image = models.ImageField(upload_to='static/images/', blank=True)
    designation = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=50)
    linkedIn_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)

    @property
    def team(self):
        return '{} : {} : {}'.format(self.committee_type, self.designation, self.name)

    def __str__(self):
        return self.committee_type


class Tags(models.Model):
    class Meta:
        verbose_name_plural = 'Tags'

    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag


class Sub_Tags(models.Model):
    class Meta:
        verbose_name_plural = 'Sub_Tags'

    sub_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.sub_tag


class Resources(models.Model):
    class Meta:
        verbose_name_plural = 'Resources'

    tag = models.ForeignKey(Tags, default=1, on_delete=models.CASCADE)
    sub_tag = models.ForeignKey(Sub_Tags, default=1, on_delete=models.CASCADE)
    PDF_description = models.CharField(max_length=200, blank=True)
    PDF = models.FileField(upload_to='static/images/', blank=True)
    Video_description = models.CharField(max_length=200, blank=True)
    Video = models.FileField(upload_to='static/images/', blank=True)
    Reference_Link = models.URLField(max_length=200, blank=True)
    created_date = models.DateField(editable=True, default=date.today)

    @property
    def resource(self):
        return '{} : {}'.format(self.tag, self.sub_tag)

    def save(self, *args, **kwargs):
        addresslist = Newsletter.objects.all().values_list('email')
        fromaddr = 'nancy.r@ahduni.edu.in'
        for address in addresslist:
            toaddrs = address
            TEXT = 'Check our latest and updated Resources on our PClub website. Hurry up !!!'
            SUBJECT = 'Programming Club Website Resources Updated'
            msg = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
            # Your gmail Credentials
            username = 'nancy.r@ahduni.edu.in'
            password = '9824228740'

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            print("mail sent")

        super().save(*args, **kwargs)


# class BlogComments(models.Model):
#     firstname = models.CharField(max_length=100,blank=True)
#     lastname = models.CharField(max_length=100,blank=True)
#     email = models.EmailField(blank=True)
#     comment = models.CharField(max_length=10000,blank=True)

class Newsletter(models.Model):
    class Meta:
        verbose_name_plural = 'Newsletter'

    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email
