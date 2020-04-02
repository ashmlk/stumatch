from .models import Comment, Course, Post, Images
from django import forms
from django.core.validators import RegexValidator
from django.forms import Textarea

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed.')
alphabetical = RegexValidator(r'^[a-zA-Z ]+$', 'Only alphanumeric characters are allowed.')

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class PostForm(forms.ModelForm):
    content= forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'What do you want to share?',
                'style': 'resize:none',
                'rows': 5 ,
                'cols': 40}))
    class Meta:
        model = Post
        fields = ('title','content',)

def image_create_uuid_p_u(instance, filename):
    return '/'.join(['post_images', str(instance.post.id), str(uuid.uuid4().hex + ".png")]) 
   
class ImageForm(forms.ModelForm):
    image = forms.FileField(
        label='',
        widget = forms.FileInput(
        	attrs={
                'required': False})) 
    class Meta:
        model = Images
        fields = ('image', )

        
class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=250,
        label='',
        widget=forms.Textarea(
            attrs={
                'style':'border-radius: 1.2rem; resize:none; outline:none;',
                'class':'form-control',
                'placeholder':'Add a comment',
                'rows': 1 ,
                'cols': 38}))
    class Meta:
        model = Comment
        fields = ('body',)
    
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(
		label='',
		max_length=12,
		min_length=5,
		required=True,
  		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Course Code",
				"class": "form-control"
			}
		)
	)
    
    instructor = forms.CharField(
		label='', 
		max_length=50,
		min_length=2,
		required=True,
  		validators=[alphabetical],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Instructor Lastname",
				"class": "form-control"
			}
		)
	)
    
    university = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=False,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "University",
				"class": "form-control"
			}
		)
	)
    
    course_semester = forms.TypedChoiceField(
        label='',
		required=False,
        choices=['spring','summer','fall','winter'],
		validators=[alphabetical],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Term",
				"class": "form-control"
			}
		)
    )


    course_year = forms.TypedChoiceField(
        coerce=int,
        choices=year_choices,
        initial=current_year,
        widget=forms.TextInput(
		    attrs={
				"placeholder": "Term",
				"class": "form-control"
			}
		)
    )
    
    class Meta:
        model = Course
        fields=('course_code','course_instructor','course_semester','course_year',)
        