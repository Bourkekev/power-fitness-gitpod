# Generated by Django 3.1.3 on 2020-11-24 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_email',
        ),
    ]
