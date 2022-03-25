from django.utils import timezone
from .models import Certificate

def my_scheduled_job():
    expired_certfiicates = Certificate.objects.filter(expiry__lte=timezone.now())
    if expired_certfiicates.count() > 0:
        for certificate in expired_certfiicates:
            certificate.approved = False
            certificate.save()
            student = certificate.students
            certificate.course.credits.filter(students=student).delete()
            student.submissions.filter(course=certificate.course).delete()
            