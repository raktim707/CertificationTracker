from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from courses.models import Certificate, Credit, AssignmentSubmission, Course
from django.forms import DateField, widgets


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['course', 'activity', 'contents', 'hours',
                  'organizer', 'program_start_date', 'program_end_date', 'organizer_name', 'organizer_address', 'organizer_website']
        widgets = {
            'program_start_date': widgets.DateInput(attrs={'type': 'date'}),
            'program_end_date': widgets.DateInput(attrs={'type': 'date'}),
            'organizer_name': widgets.HiddenInput(),
            'organizer_address':  widgets.HiddenInput(),
            'organizer_website': widgets.HiddenInput(),
             }

class AssignmentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.exclude(assignment=''), label='Course')
    file = forms.FileField()