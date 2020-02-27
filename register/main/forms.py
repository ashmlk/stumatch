from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from main.models import Profile

class SignUpForm(UserCreationForm):
	username = forms.CharField(
		label='',
		max_length=30,
		min_length=4,
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
		model = Profile
		fields = ('username', 'first_name', 'last_name', 'email','university',) 

		def __init__(self,*args,**kwargs):
				super().__init__(*args,**kwargs)
				for field in self.fields:
						self.fields[field].widget.attrs.update({'class':'form-control','placeholder':self.fields[field].label})
                		
class EditProfileForm(UserChangeForm):
    
	username = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=False,
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
    
	bio = forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
				"placeholder":"Enter something about yourself",
				"class": "form-control"
			}
		)
	)
	

	password = None

	class Meta:
		model = Profile
		fields=('username','first_name','last_name','email','bio',)
		def save(self, commit = True):
			user = super(UserChangeForm, self).save(commit=False)
			user.bio = self.cleaned_data['bio']

			if commit:
				user.save()
			return user
        

class PasswordResetForm(PasswordChangeForm):

	class Meta:
		model = Profile
		fields = ('old_password','new_password1','new_password2')
