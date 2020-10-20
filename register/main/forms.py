from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from main.models import Profile, ReportUser, ReportPost, ReportComment, ReportBuzz, ReportBuzzReply, ReportBlog, ReportBlogReply, ReportCourseReview
from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput
from django.forms import Select
from django.contrib.auth.hashers import check_password
from datetime import datetime, timezone
from django.utils import timezone


username_regex =  RegexValidator(r'^(?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9._ ]+$', 'You may only use alphanumeric characters and/or dots and hyphen (Consecutive dots are not allowed)')
alphanumeric = RegexValidator(r"^(?:[^\W_]|[ '-])+$", 'Only alphanumeric characters are allowed.')

UNIVERSITY_CHOICES = (
		('University',
   			(
				   		("","University"),
						("Acadia University","Acadia University"),
						("Alberta University of the Arts","Alberta University of the Arts"),
						("Algoma University","Algoma University"),
						("Athabasca University","Athabasca University"),
						("Atlantic School of Theology","Atlantic School of Theology"),
						("Bishop's University","Bishop's University"),
						("Booth University College","Booth University College"),
						("Brandon University","Brandon University"),
						("Brock University","Brock University"),
						("Canadian Mennonite University","Canadian Mennonite University"),
						("Cape Breton University","Cape Breton University"),
						("Capilano University","Capilano University"),
						("Carleton University","Carleton University"),
						("Concordia University","Concordia University"),
						("Crandall University","Crandall University"),
						("Dalhousie University","Dalhousie University"),
						("Emily Carr University of Art and Design","Emily Carr University of Art and Design"),
						("Fairleigh Dickinson University","Fairleigh Dickinson University"),
						("Institut national de la recherche scientifique","Institut national de la recherche scientifique"),
						("Kingswood University","Kingswood University"),
						("Kwantlen Polytechnic University","Kwantlen Polytechnic University"),
						("Lakehead University","Lakehead University"),
						("Laurentian University","Laurentian University"),
						("MacEwan University","MacEwan University"),
						("McGill University","McGill University"),
						("McMaster University","McMaster University"),
						("Memorial University of Newfoundland","Memorial University of Newfoundland"),("Mount Allison University","Mount Allison University"),
						("Mount Royal University","Mount Royal University"),("Mount Saint Vincent University","Mount Saint Vincent University"),
						("New York Institute of Technology","New York Institute of Technology"),("Niagara University","Niagara University"),("Nipissing University","Nipissing University"),
						("Nova Scotia College of Art and Design University","Nova Scotia College of Art and Design University"),
						("Ontario College of Art and Design University","Ontario College of Art and Design University"),("Ontario Tech University","Ontario Tech University"),
						("Queen's University at Kingston","Queen's University at Kingston"),("Quest University","Quest University"),
						("Redeemer University College","Redeemer University College"),("Royal Military College of Canada" 
						,"Royal Military College of Canada"),
						("Royal Roads University","Royal Roads University"),
						("Ryerson University","Ryerson University"),( 
						"Saint Francis Xavier University","Saint Francis Xavier University"),
						("Saint Mary's University","Saint Mary's University"),("Simon Fraser University","Simon Fraser University"),
						("St. Stephen's University","St. Stephen's University"),
						("St. Thomas University","St. Thomas University"),("The King's University","The King's University"),
						("Thompson Rivers University","Thompson Rivers University"),("Trent University","Trent University"),
						("Trinity Western University","Trinity Western University"),
						("Tyndale University","Tyndale University") 
						,("University Canada West","University Canada West"),
						("University College of the North","University College of the North"),("University of Alberta","University of Alberta"),
						("University of British Columbia","University of British Columbia"),
						("University of Calgary","University of Calgary"),
						("University of Fredericton","University of Fredericton"),("University of Guelph","University of Guelph"),("University of King's College","University of King's College"),
						("University of Lethbridge","University of Lethbridge"),("University of Manitoba","University of Manitoba"),
						("University of New Brunswick","University of New Brunswick"),("University of Northern British Columbia","University of Northern British Columbia"),
						("University of Ottawa","University of Ottawa"),("University of Prince Edward Island","University of Prince Edward Island"),("University of Regina","University of Regina"),
						("University of Saskatchewan","University of Saskatchewan"),("University of Toronto","University of Toronto"),
						("University of Victoria","University of Victoria"),
						("University of Waterloo","University of Waterloo"),("University of Western Ontario","University of Western Ontario"),("University of Windsor","Universityof Windsor"),("University of Winnipeg","University of Winnipeg"),
						("University of the Fraser Valley","University of the Fraser Valley"),
						("Université Laval","Université Laval"),("Université Sainte-Anne","Université Sainte-Anne"),("Université de Moncton","Université de Moncton"),("Université de Montréal","Université de Montréal"),
						("Université de Sherbrooke","Université de Sherbrooke"),
						("Université de l'Ontario français","Université de l'Ontario français"),
						("Université du Québec en Abitibi-Témiscamingue","Université du Québec en Abitibi-Témiscamingue"),("Université du Québec en Outaouais","Université du Québec en Outaouais"),
						("Université du Québec à Chicoutimi","Université du Québec à Chicoutimi"),
						("Université du Québec à Montréal","Université du Québec à Montréal"),("Université du Québec à Rimouski","Université du Québec à Rimouski"),
						("Université du Québec à Trois-Rivières","Université du Québec à Trois-Rivières"),("Vancouver Island University","Vancouver Island University"),
						("Wilfrid Laurier University","Wilfrid Laurier University"),("York University","York University"),("Yukon University","Yukon University"),
						("École de technologie supérieure","École de technologie supérieure"),
						("École nationale d'administration publique","École nationale d'administration publique"),
			)
		),
)

class MySelect(Select):
    def create_option(self, *args,**kwargs):
        option = super().create_option(*args,**kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=200
        )
    email = forms.EmailField()
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
				"class": "form-control mb-2"
			}
		)
	)

	first_name = forms.CharField(
		label='',
		max_length=50,
		min_length=1,
		required=True,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "First name",
				"class": "form-control mb-2"
			}
		)
	)

	last_name = forms.CharField(
		label='',
		max_length=50,
		min_length=1,
		required=True,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Last name",
				"class": "form-control mb-2"
			}
		)
	)
 
	email = forms.EmailField(
		label='',
		max_length=200,
		required=True,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control mb-2"
			}
		)
	)

	university = forms.ChoiceField(
		label='',
		required=True,
  		choices = UNIVERSITY_CHOICES,

  		widget=MySelect(
        attrs={
			"class":"form-control mb-2"
		}
        ), 
	)

	password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Password",
				"class": "form-control mb-2"
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
				"class": "form-control mb-2"
			}
		)
	)
 
	error_css_class = "error"
 

	class Meta:
		model = Profile
		fields = ('username', 'first_name', 'last_name', 'email','university',) 

		def __init__(self,*args,**kwargs):
				super().__init__(*args,**kwargs)
				for field in self.fields:
						self.fields[field].widget.attrs.update({'class':'form-control','placeholder':self.fields[field].label})
      
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if Profile.objects.filter(username=username).exists():
				if Profile.objects.filter(username=username, is_active=False).exists():
					p = Profile.objects.filter(username=username, is_active=False).delete()
				elif Profile.objects.filter(username=username, is_active=True).exists():
					raise forms.ValidationError("A user with this username already exists.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if Profile.objects.filter(email=email).exists():
				if Profile.objects.filter(email=email, is_active=False).exists():
					p = Profile.objects.filter(email=email, is_active=False).delete()
				elif Profile.objects.filter(email=email, is_active=True).exists():
					raise forms.ValidationError("A user with this email already exists.")
		return email
                		
class EditProfileForm(UserChangeForm):
    
	username = forms.CharField(
		max_length=255,
		min_length=1,
		required=False,
		validators=[username_regex],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
				"class": "form-control mb-2",
				
			}
		)
	)

	first_name = forms.CharField(
		max_length=255,
		min_length=1,
		required=False,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "First name",
				"class": "form-control mb-2",
    			
			}
		)
	)

	last_name = forms.CharField(
		max_length=255,
		min_length=1,
		required=False,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Last name",
				"class": "form-control mb-2",
    			
			}
		)
	)
	'''
	email = forms.EmailField(

		required=False,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control mb-2",
    		
			}
		)
	)
 	'''
    
	bio = forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
				"placeholder":"Enter something about yourself",
				"class": "form-control mt-3",
				"rows":"5",
    		
			}
		)
	)


  
	password = None

	error_css_class = "error"
 
	class Meta:
		model = Profile
		fields=('username','first_name','last_name','bio',)


class SetUniversityForm(forms.ModelForm):
    
    program = forms.CharField(
        label = '',
		required=False,
		widget=forms.TextInput(
			attrs={
				"placeholder":"What are you studying?",
				"class": "form-control",
			}
		)
	)
    
    university = forms.ChoiceField(
		label='',
		required=True,
  		choices = UNIVERSITY_CHOICES,
  		widget=MySelect(
        attrs={
			"class":"form-control",
			
		}
        ), 
	)
    
    class Meta:
        model = Profile
        fields = ('university','program')
    
    def signup(self, request, user):
        user.university = self.cleaned_data['university']
        user.program = self.cleaned_data['program']
        user.save()
      

class PasswordResetForm(PasswordChangeForm):

	class Meta:
		model = Profile
		fields = ('old_password','new_password1','new_password2')
  
  
class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
			attrs={
				"class": "form-control",
			}
		)
        )

    class Meta:
        model = Profile
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
    
class ReportUserForm(forms.ModelForm):
    
    class Meta:
        model = ReportUser
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}
        
class ReportPostForm(forms.ModelForm):
    
    class Meta:
        model = ReportPost
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}

class ReportCommentForm(forms.ModelForm):
    
    class Meta:
        model = ReportComment
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}

class ReportBuzzForm(forms.ModelForm):
    
    class Meta:
        model = ReportBuzz
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}
        
class ReportBuzzReplyForm(forms.ModelForm):
    
    class Meta:
        model = ReportBuzzReply
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}        
        
class ReportBlogForm(forms.ModelForm):
    
    class Meta:
        model = ReportBlog
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}   

class ReportBlogReplyForm(forms.ModelForm):
    
    class Meta:
        model = ReportBlogReply
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}
        
class ReportCourseReviewForm(forms.ModelForm):
    
    class Meta:
        model = ReportCourseReview
        fields = ('reason',)
        widgets = {'reason':forms.RadioSelect}        

        
        
