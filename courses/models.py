from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from embed_video.fields import EmbedVideoField
from .fields import OrderField

organizer_choices = [
    ('ward', 'WARD'),
    ('others', 'Others')
]


class Organizer(models.Model):
    name = models.CharField(max_length=200, default='WARD')
    website = models.URLField(default=None)
    country = models.CharField(max_length=300, default=None)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    organizer = models.CharField(max_length=100, choices=organizer_choices)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    students = models.ManyToManyField(
        User, related_name='courses_joined', blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_hours = models.IntegerField()
    assignment = models.FileField(upload_to='assignments/', blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

class Activity(models.Model):
    course = models.ForeignKey(
        Course, related_name='activites', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    activity = models.ForeignKey(
        Activity, related_name='contents', on_delete=models.CASCADE)
    title = models.TextField()
    order = OrderField(blank=True, for_fields=['activity'])

    class Meta:
        ordering = ['order']



'''class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate()'''

class Certificate(models.Model):
    course = models.ForeignKey(
        Course, related_name='certificates', on_delete=models.CASCADE, null=True)
    students = models.ForeignKey(
        User, related_name='certificates', on_delete=models.CASCADE)
    created_at = models.DateField(null=True, blank=True)
    reissued_date = models.DateField(null=True, blank=True)
    expiry = models.DateField(default=None)
    approved = models.BooleanField(default=False)
    program_end_date = models.DateField(null=True)
    program_start_date = models.DateField(null=True)
    organizer = models.CharField(max_length=100, choices=organizer_choices, default='ward')
    organizer_name = models.CharField(max_length=200, null=True, blank=True)
    organizer_address = models.CharField(max_length=300, null=True, blank=True)
    organizer_website = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.course.title
    


class Credit(models.Model):
    hours = models.IntegerField()
    activity = models.CharField(max_length=300, default=None)
    contents = models.TextField(default=None)
    course = models.ForeignKey(
        Course, related_name='credits', on_delete=models.CASCADE)
    students = models.ForeignKey(
        User, related_name='credits', on_delete=models.CASCADE)
    approved_date = models.DateField(default=None, null=True, blank=True)
    approved = models.BooleanField(default=False)
    program_start_date = models.DateField(default=None, null=True)
    program_end_date = models.DateField(default=None, null=True)
    organizer = models.CharField(max_length=100, choices=organizer_choices)
    organizer_name = models.CharField(max_length=200, null=True, blank=True)
    organizer_address = models.CharField(max_length=400, null=True, blank=True)
    organizer_website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.course.title

class AssignmentSubmission(models.Model):
    course = models.ForeignKey(Course, related_name='submissions', on_delete=models.CASCADE)
    students = models.ForeignKey(User, related_name='submissions',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='studentSubmission/', null=True)
    point = models.IntegerField(null=True, blank=True, default=0)
    approved_date = models.DateField(blank=True, null=True, default=None)
    def __str__(self):
        return self.students.username

'''
class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    content = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.ImageField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()'''
