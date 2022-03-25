from django import template
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from courses.models import Certificate
import datetime

register = template.Library()

@register.filter(name='total_assignments')
def total_assignments(user):
    if user.is_authenticated:
        courses = user.courses_joined.exclude(assignment='')
        total = courses.count()
        user_submissions = user.submissions.filter(course__in=courses).count()
        pending = total - user_submissions
        return pending
    else:
        return ''
    