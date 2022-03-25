from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'students'

urlpatterns=[
    path('', views.StudentCourseListView.as_view(), name='course_list'),
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('<int:pk>/courses/', views.StudentCourseDetailView, name='course_detail'),
    path('credit-application/', views.CreditFormView.as_view(), name='credit_application'),
    path('my-certificates/', views.certificateListView, name='my_certificates'),
    path('assignments/', views.assignmentView, name='assignments'),
    path('my-submissions/', views.assignmentFormView, name='student_submission'),
    path('<int:id>/certificate', views.certificateReciept, name='pdf_certificate'),
    path('search/', views.searchView, name='all_search'),
]
