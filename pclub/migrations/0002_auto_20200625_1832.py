# Generated by Django 3.0.7 on 2020-06-25 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pclub', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventgallery',
            options={'verbose_name_plural': 'Event Gallery'},
        ),
        migrations.AlterModelOptions(
            name='events',
            options={'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='homepageimages',
            options={'verbose_name_plural': 'HomePage Images'},
        ),
        migrations.AlterModelOptions(
            name='teams',
            options={'verbose_name_plural': 'Teams'},
        ),
    ]
