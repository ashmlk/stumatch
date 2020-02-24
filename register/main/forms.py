from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    university = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','university', 'password1', 'password2',)
    
class AddNewCourse(forms.Form):
    course_code = forms.CharField(max_length=20)
    course_instructor =forms.CharField(max_length=200)
    date_taken = forms.DateField()
