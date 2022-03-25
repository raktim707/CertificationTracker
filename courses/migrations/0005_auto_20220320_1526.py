# Generated by Django 3.2.5 on 2022-03-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20220320_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='organizer_address',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='credit',
            name='organizer_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='credit',
            name='organizer_website',
            field=models.URLField(null=True),
        ),
    ]
