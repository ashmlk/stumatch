from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from main.models import (
    Profile,
    ReportUser,
    ReportPost,
    ReportComment,
    ReportBuzz,
    ReportBuzzReply,
    ReportBlog,
    ReportBlogReply,
    ReportCourseReview,
)
from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput
from django.forms import Select
from django.contrib.auth.hashers import check_password
from datetime import datetime, timezone
from django.contrib.auth import password_validation
from django.utils import timezone
from assets.assets import UNIVERSITY_CHOICES_SIGNUP, UNIVERSITY_CHOICES
from helper.generate_user_identity import generate_username, get_first_last_name

username_regex = RegexValidator(
    r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)",
    "You may only use alphanumeric characters and/or dots and hyphen (Consecutive dots are not allowed)",
)
alphanumeric = RegexValidator(
    r"^(?:[^\W_]|[ '-])+$", "Only alphanumeric characters are allowed."
)

class MySelect(Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get("value"):
            option["attrs"]["disabled"] = "disabled"

        return option


class ContactForm(forms.Form):
    name = forms.CharField(
        label="",
        required=True,
        min_length=1,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Full name"}),
    )
    email = forms.EmailField(
        label="",
        max_length=200,
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control mb-2"}
        ),
    )
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):

    username = forms.CharField(
		label='',
		max_length=30,
		min_length=1,
		required=True,
  		validators=[username_regex],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
                "autofocus":None
			}
		)
	)
    """
    full_name = forms.CharField(
        label="",
        max_length=300,
        min_length=1,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={"placeholder": "Full Name", }
        ),
    )
    """
    email = forms.EmailField(
        label="",
        max_length=200,
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", }
        ),
    )

    university = forms.ChoiceField(
        label="",
        required=True,
        choices=UNIVERSITY_CHOICES_SIGNUP,
        widget=MySelect(attrs={}),
    )

    password1 = forms.CharField(
        label="",
        max_length=30,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "id":"password-input-field"}
        ),
    )
    password2 = None
    
    error_css_class = "error"

    class Meta:
        model = Profile
        fields = (
            "email",
            "username",
            "university",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')

          
    def save(self, *args, **kwargs):
        user = self.cleaned_data
        first, last = get_first_last_name(self.instance.full_name)
        self.instance.first_name = first
        self.instance.last_name = last
        return super().save(*args, **kwargs)
            
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Profile.objects.filter(email=email).exists():
            if Profile.objects.filter(email=email, is_active=False).exists():
                p = Profile.objects.filter(email=email, is_active=False).delete()
            elif Profile.objects.filter(email=email, is_active=True).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email


class EditProfileForm(UserChangeForm):

    username = forms.CharField(
        max_length=30,
        min_length=1,
        required=True,
        validators=[username_regex],
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control mb-2",}
        ),
    )

    full_name = forms.CharField(
        label="Full Name",
        max_length=300,
        min_length=1,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={"placeholder": "Full Name", "class": "form-control "}
        ),
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter something about yourself",
                "class": "form-control mt-3",
                "rows": "5",
            }
        ),
    )

    password = None

    error_css_class = "error"

    class Meta:
        model = Profile
        fields = (
            "username",
            "full_name",
            "bio",
        )

class SetUniversityForm(forms.ModelForm):

    program = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "What are you studying?", "class": "form-control",}
        ),
    )

    university = forms.ChoiceField(
        label="",
        required=True,
        choices=UNIVERSITY_CHOICES_SIGNUP,
        widget=MySelect(attrs={"class": "form-control",}),
    )

    class Meta:
        model = Profile
        fields = ("university", "program")

    def signup(self, request, user):
        user.university = self.cleaned_data["university"]
        user.program = self.cleaned_data["program"]
        user.save()


class PasswordResetForm(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = ("old_password", "new_password1", "new_password2")


class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",})
    )

    class Meta:
        model = Profile
        fields = ("confirm_password",)

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get("confirm_password")
        if not check_password(confirm_password, self.instance.password):
            self.add_error("confirm_password", "Password does not match.")

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class ReportUserForm(forms.ModelForm):
    class Meta:
        model = ReportUser
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportPostForm(forms.ModelForm):
    class Meta:
        model = ReportPost
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportBuzzForm(forms.ModelForm):
    class Meta:
        model = ReportBuzz
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportBuzzReplyForm(forms.ModelForm):
    class Meta:
        model = ReportBuzzReply
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportBlogForm(forms.ModelForm):
    class Meta:
        model = ReportBlog
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportBlogReplyForm(forms.ModelForm):
    class Meta:
        model = ReportBlogReply
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}


class ReportCourseReviewForm(forms.ModelForm):
    class Meta:
        model = ReportCourseReview
        fields = ("reason",)
        widgets = {"reason": forms.RadioSelect}
