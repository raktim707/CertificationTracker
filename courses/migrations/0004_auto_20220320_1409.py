# Generated by Django 3.2.5 on 2022-03-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20220320_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='organizer_address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizer_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='organizer_website',
            field=models.URLField(null=True),
        ),
    ]