# Generated by Django 3.2.5 on 2022-03-20 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='organizer',
        ),
    ]