# Generated by Django 3.2.5 on 2022-03-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='file',
            field=models.FileField(null=True, upload_to='studentSubmission/'),
        ),
    ]
