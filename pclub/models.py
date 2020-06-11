from django.db import models

CATEGORIES = (
    ('Secretary','Secretary'),
    ('Joint Secretary','Joint Secretary'),
    ('Treasurer','Treasurer'),
)


class HomepageImages(models.Model):
    image = models.ImageField(upload_to='static/images/')


class Events(models.Model):
    event_date = models.DateField()
    event_name = models.CharField(max_length=200)
    event_info = models.TextField()
    event_url = models.URLField(blank=True)

    def __str__(self):
        return self.event_name


class Teams(models.Model):
    image = models.ImageField(upload_to='static/images/')
    designation = models.CharField(choices=CATEGORIES, max_length=20)
    name = models.CharField(max_length=50)
    linkedIn_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)

    def _str_(self):
        return self.designation
