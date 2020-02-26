class EditProfileForm(UserChangeForm):

    university = forms.CharField(
        max_length=30,
        min_length=4)

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

    class Meta:
	    model = User
	    fields = ('first_name', 'last_name', 'email','university',)

class ResetPasswordForm(PasswordChangeForm):
        old_password = forms.CharField(required=True)
        new_password1 = forms.CharField(required=True)
        new_password2 = forms.CharField(required=True)

    class Meta:
	    model = User
	    fields = ('old_password', 'new_password1', 'new_password2',)

		def save(self, commit=True):             
		    user = super(PasswordChangeForm, self).save(commit=True)
            if commit:
               user.save()
            return user
	class Meta:
		model = User
		fields = ('old_password,new_password1,new_password2,)

        def save(self, commit=True):
            user = super(PasswordChangeForm, self).save(commit=True)
            if commit:
               user.save()
            return user