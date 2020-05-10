from .models import Comment, Course, Post, Images, Review
from django import forms
from django.core.validators import RegexValidator
from django.forms import Textarea
import datetime

alphanumeric_v2 = RegexValidator(r'^(?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9. ]+$', 'You may only use alphanumeric characters and/or dots (Consecutive dots are not allowed)')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed( No spaces ).')
alphabetical = RegexValidator(r'^[a-zA-Z ]+$', 'Only alphabetical characters are allowed.')

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Set an interesting title!'
                }))
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
    
    def __init__(self, *args, **kwargs): 
        super(PostForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:                     
            self.fields['title'].disabled = True
   
class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
                'class':'image_upload_form'
                }))
    class Meta:
        model = Images
        fields = ('image',)

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
                'cols': 60}))
    class Meta:
        model = Comment
        fields = ('body',)
        
class ReviewForm(forms.ModelForm):
    body = forms.CharField(
        max_length=400,
        label='',
        widget=forms.Textarea(
            attrs={
                'style':'resize:none; outline:none;',
                'class':'form-control',
                'placeholder':'Write a review and let other know your experience!',
                'rows': 4 ,
                'cols': 80}))
    class Meta:
        model = Review
        fields = ('body',)
    
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(
		label='',
		max_length=12,
		min_length=5,
		required=True,
  		validators=[alphanumeric_v2],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Course Code",
				"class": "form-control"
			}
		)
	)
    
    course_instructor = forms.CharField(
		label='', 
		max_length=50,
		min_length=2,
		required=True,
  		validators=[alphabetical],
        help_text='Please ommit any title(Dr., Professor, Mr., Mrs.,...)',
		widget=forms.TextInput(
			attrs={
				"placeholder": "Instructor Lastname",
				"class": "form-control"
			}
		)
	)
    
    course_university = forms.CharField(
		label='',
		max_length=50,
		min_length=2,
		required=True,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Enter University",
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
				"placeholder": "When did you take this course?",
				"class": "form-control"
			}
		)
    )
    
    class Meta:
        model = Course
        fields=('course_code','course_university','course_instructor','course_year','course_semester','course_difficulty',)
        