from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Profile


class SignUpForm(UserCreationForm):
    university = forms.CharField(
        max_length=30,
        min_length=4)

    username = forms.CharField(
		label='',
		max_length=30,
		min_length=5,
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
				"class": "form-control"
			}
		)
	)

    first_name = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "First name",
				"class": "form-control"
			}
		)
	)

    last_name = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Last name",
				"class": "form-control"
			}
		)
	)

    university = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=False,
		widget=forms.TextInput(
			attrs={
				"placeholder": "University",
				"class": "form-control"
			}
		)
	)

    email = forms.EmailField(
		label='',
		max_length=255,
		required=True,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)

    password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Password",
				"class": "form-control"
			}
		)
	)

    password2 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Confirm Password",
				"class": "form-control"
			}
		)
	)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','university', 'password1', 'password2',)

        def save(self, commit=True):
            user = super(UserCreateForm, self).save(commit=True)
            user.extra_field = self.cleaned_data["university"]
            if commit:
               user.save()
            return user

class AddNewCourse(forms.Form):
    course_code = forms.CharField(max_length=20)
    course_instructor =forms.CharField(max_length=200)
    date_taken = forms.DateField()
