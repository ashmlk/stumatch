from .models import Comment, Course
from django import forms
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed.')
alphabetical = RegexValidator(r'^[a-zA-Z ]+$', 'Only alphanumeric characters are allowed.')

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'username', 'body')
      
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(
        normalize = lambda x: x.replace(' ','').upper(),
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
        normalize = lambda x: x.strip(),
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
        normalize = lambda x: x.strip(),
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
    
    course_semester = forms.TypeChoiceField(
        label='',
		max_length=5,
		min_length=4,
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
        fields=('course_code','course_instructor','course_semester','course_year')
        