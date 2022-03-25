from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, CreditForm, AssignmentForm
from courses.models import Course, Credit, AssignmentSubmission, Certificate
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('students:course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

@login_required(redirect_field_name='login')
def StudentCourseDetailView(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    credits = []
    if user in course.students.all():
        credits = user.credits.filter(course=course, approved=True)
        assignment = user.submissions.filter(course=course).exclude(point=0)
        total_credits = credits.aggregate(Sum('hours'))['hours__sum']
        if assignment.count()>0:
            if total_credits:
                total_credits = assignment[0].point + int(total_credits)
            else:
                total_credits=assignment[0].point

    return render(request, 'students/course/detail.html', {'credits': credits, 'course': course, 'total_credits': total_credits, 'assignments': assignment})


class CreditFormView(LoginRequiredMixin, FormView):
    template_name = 'students/credit_application.html'
    form_class = CreditForm
    success_url = reverse_lazy('students:course_list')

    def form_valid(self, form):
        course = form.data['course']
        course = get_object_or_404(Course, pk=course)
        activity = form.data['activity']
        contents = form.data['contents']
        hours = form.data['hours']
        organizer = form.data['organizer']
        program_start_date = form.data['program_start_date']
        program_end_date = form.data['program_end_date']
        student = self.request.user
        if course:
            if student not in course.students.all():
                course.students.add(student)
                course.save()
            Credit.objects.create(course=course, students=student,
                                  activity=activity, contents=contents, hours=hours, organizer=organizer,
                                  program_start_date=program_start_date, program_end_date=program_end_date,
                                  approved=False)
            messages.success(self.request, 'Successfully Submitted Application for Credit')
        return super().form_valid(form)


def assignmentFormView(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.data['course']
            student = request.user
            course =get_object_or_404(Course, pk=course)
            if student not in course.students.all():
                course.students.add(student)
                course.save()
            file=request.FILES['file']
            AssignmentSubmission.objects.create(course=course, file=file, students=student)
            messages.success(request, 'Assignments submission successful')
            return redirect('/')
    else:
        form = AssignmentForm()
    return render(request, 'students/student/submission.html', {'form':form})

@login_required(redirect_field_name='login')
def certificateListView(request):
    student = request.user
    certificates = student.certificates.filter(approved=True)
    expired_certificates = student.certificates.filter(expiry__lte=timezone.now())
    print(expired_certificates)
    return render(request, 'students/student/certificates.html', {'certificates': certificates, 'expired_certificates': expired_certificates})

@login_required(redirect_field_name='login')
def assignmentView(request):
    student = request.user
    courses = Course.objects.filter(students=student).exclude(assignment='')
    return render(request, 'students/course/assignments.html', {'courses': courses})

@login_required(redirect_field_name='login')
def searchView(request):
    query = request.GET.get('search')
    student = request.user
    courses = []
    certificates=[]
    if query:
        courses = Course.objects.filter(title__icontains=query, students=student)
        certificates = Certificate.objects.filter(course__title__icontains=query, students=student)
    return render(request, 'students/search_result.html', { 'query': query, 'courses':courses, 'certificates': certificates})

def certificateReciept(request, id):
    certificate = get_object_or_404(Certificate, id=id)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename={course}-certificate.pdf".format(
    course=certificate.course,)
    html = render_to_string("students/student/pdf_certificate.html", {'certificate': certificate,})
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response