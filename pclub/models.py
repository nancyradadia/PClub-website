from django.db import models


class HomepageImages(models.Model):
    image = models.ImageField(upload_to='static/images/')




