from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from main.models import Profile
from .models import User

class SignUpForm(UserCreationForm):

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
        fields = ('username', 'first_name', 'last_name', 'email','university',)

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=True)
            user.extra_field = self.cleaned_data["university"]
            if commit:
               user.save()
            return user


class EditProfileForm(UserChangeForm):

    first_name = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=False,
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
		required=False,
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
		required=False,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)

    password = None

    class Meta:
	    model = User
	    fields = ('first_name', 'last_name', 'email','university',)




class PasswordResetForm(PasswordChangeForm):
	old_password = forms.CharField(required=True, widget=forms.PasswordInput())
	new_password1 = forms.CharField(required=True, widget=forms.PasswordInput())
	new_password2 = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('old_password','new_password1','new_password2')
