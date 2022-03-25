from django.contrib import admin
from .models import Organizer, Course, Activity, Content, Certificate, Credit, AssignmentSubmission
import datetime
from django.db.models import Sum

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'total_hours', 'assignment']
    search_fields = ['title', 'organizer', 'students__first_name', 'students__last_name']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    search_fields = ['students__first_name', 'students__last_name', 'course__title']
    list_display = ['students', 'course', 'created_at', 'approved', 'expiry']
    list_filter = ['course', 'approved', 'expiry']

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ['students', 'course', 'activity', 'approved', 'hours']
    search_fields = ['students__first_name', 'students__last_name', 'course__title', 'activity']
    list_filter = ['course', 'approved']
    def save_model(self, request, obj, form, change):
        isApproved = form.cleaned_data['approved']
        if isApproved == True:
            obj.approved = True
            obj.approved_date = datetime.date.today()
            obj.save()
            student = obj.students
            all_credits = student.credits.filter(
                course=obj.course, approved=True)
            print('all_credits: ', all_credits)
            
            total_credits = all_credits.aggregate(Sum('hours'))['hours__sum']
            assignment_point = student.submissions.filter(course=obj.course).aggregate(Sum('point'))['point__sum']
            if total_credits:
            	if assignment_point:
            		total_credits = int(total_credits) + int(assignment_point)
            		print('hhsd: ', total_credits)
            	else:
            		total_credits = int(total_credits)
            if total_credits == obj.course.total_hours:
                my_certificate = student.certificates.filter(course=obj.course)
                if my_certificate.count() ==0:
                    created_at = datetime.date.today()
                    expiry = created_at.replace(created_at.year + 3)
                    start_date=obj.course.start_date
                    end_date = obj.course.end_date
                    organizer = obj.course.organizer
                    Certificate.objects.create(course=obj.course, students=student, created_at=created_at, expiry=expiry, approved=True, program_start_date=start_date, program_end_date=end_date)
                
                elif my_certificate.count() > 0:
                    expired_certificate = my_certificate[0]
                    if expired_certificate.expiry < datetime.date.today():
                        reissued_date=datetime.date.today()
                        expiry = reissued_date.replace(reissued_date.year + 3)
                        start_date=obj.course.start_date
                        end_date = obj.course.end_date
                        expired_certificate.reissued_date = reissued_date
                        expired_certificate.approved =True
                        expired_certificate.expiry = expiry
                        expired_certificate.program_start_date=start_date
                        expired_certificate.program_end_date=end_date
                        expired_certificate.save()
                        
        super().save_model(request, obj, form, change)

@admin.register(AssignmentSubmission)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['students', 'course', 'point', 'file']
    search_fields = ['students__first_name', 'students__last_name', 'course__title']
    def save_model(self, request, obj, form, change):
        point = form.cleaned_data['point']
        approved_date = datetime.date.today()
        obj.approved_date = approved_date
        obj.save()
        student = obj.students
        all_credits = student.credits.filter(course=obj.course, approved=True)
        total_credits = all_credits.aggregate(Sum('hours'))['hours__sum']
        if total_credits:
            total_credits = int(total_credits) + point
        else:
            total_credits = point
        print('total: ', total_credits)
        if total_credits == obj.course.total_hours:
            print('gotcha')
            my_certificate = student.certificates.filter(course=obj.course)
            print(my_certificate)
            if my_certificate.count()==0:
                created_at = datetime.date.today()
                expiry = created_at.replace(created_at.year + 3)
                start_date=obj.course.start_date
                end_date = obj.course.end_date
                organizer = obj.course.organizer
                Certificate.objects.create(course=obj.course, students=student, expiry=expiry, created_at=created_at , approved=True, program_start_date=start_date, program_end_date=end_date)
                
            elif my_certificate.count() > 0:
                expired_certificate = my_certificate[0]
                if expired_certificate.expiry < datetime.date.today():
                    print(expired_certificate)
                    reissued_date = datetime.date.today()
                    expiry = reissued_date.replace(reissued_date.year + 3)
                    start_date=obj.course.start_date
                    end_date = obj.course.end_date
                    expired_certificate.reissued_date = reissued_date
                    expired_certificate.approved = True
                    expired_certificate.expiry = expiry
                    expired_certificate.program_start_date=start_date
                    expired_certificate.program_end_date=end_date
                    expired_certificate.approved =True
                    expired_certificate.save()
                        
        super().save_model(request, obj, form, change)
        
admin.site.register(Organizer)


