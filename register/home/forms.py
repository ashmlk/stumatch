from .models import Comment, Course, Post, Images, Review, Buzz, BuzzReply, Blog, BlogReply, CourseList, CourseListObjects
from django import forms
from django.core.validators import RegexValidator
from django.forms import Textarea
import datetime
from taggit.forms import TagField
from taggit.forms import TagWidget
from dal import autocomplete
from taggit.models import Tag
from main.forms import MySelect
from main.forms import UNIVERSITY_CHOICES

alphanumeric_v2 = RegexValidator(r'^(?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9. ]+$', 'You may only use alphanumeric characters and/or dots (Consecutive dots are not allowed)')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed( No spaces ).')
alphanumeric_s = RegexValidator(r'^[0-9a-zA-Z ]+$', 'Only alphanumeric characters are allowed')
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
                'placeholder': "What's your post about?"
                }))
    content= forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write what you want to share...',
                'style': 'resize:none',
                'rows': 7,
                'cols': 40}))
    
    class Meta:
        model = Post
        labels = {
            "tags": "",
        }
        help_texts = {
            'tags': 'Tags',
        }
        fields = ('title','content','tags',)
        
    
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
                'style':'border-radius: 20px; resize:none; outline:none;',
                'class':'form-control form-control-sm',
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
                'placeholder':'Write a review and let others know about your experience!',
                'rows': 4 ,
                'cols': 80}))
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Review
        labels = {
            "review_interest": "Rating",
        }
        fields = ('body','review_interest')
    
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(
		label='',
		max_length=20,
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
        help_text='Please omit any title(Dr., Professor, Mr., Mrs.,...)',
		widget=forms.TextInput(
			attrs={
				"placeholder": "Instructor Lastname",
				"class": "form-control"
			}
		)
	)
    
    course_university = forms.ChoiceField(
		label='',
		required=True,
  		choices = UNIVERSITY_CHOICES,
  		widget=MySelect(
        attrs={
			"class":"form-control"
		}
        ), 
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
    
    error_css_class = "error"
    
    class Meta:
        model = Course
        fields=('course_code','course_university','course_instructor','course_year','course_semester','course_difficulty',)

class BuzzForm(forms.ModelForm):
    nickname = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': "Set a nickname if you like..."
                }))
    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': "What's your buzz about?"
                }))
    content= forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write it here...',
                'style': 'resize:none',
                'rows': 5,
                'cols': 40,
                'maxlength': '500',
                }),
        )
    class Meta:
        model = Buzz
        labels = {
            "tags": "",
        }
        help_texts = {
            'tags': 'Tags',
        }
        fields = ('nickname','title','content','tags',)
        

        
class BuzzReplyForm(forms.ModelForm):
    reply_nickname = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2 rounded-0",
                'placeholder': "Set a nickname if you like..."
                }))
    reply_content = forms.CharField(
        max_length=180,
        label='',
        widget=forms.Textarea(
            attrs={
                'style':'outline:none;min-height:5rem',
                'class':'form-control rounded-0',
                'placeholder':'Add a comment anonymously...',
                'rows': 2 ,
                'cols': 50}))
    class Meta:
        model = BuzzReply
        fields = ('reply_nickname','reply_content',)
        

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                "class": "form-control h4 blog-title-input",
                'placeholder': "Set Title"
                }))
    class Meta:
        model = Blog
        labels = {
            "title": "",
            "content":"",
        }
        fields = ['title', 'content','tags']
        labels = {
            "tags": "",
            "content":"",
        }
        help_texts = {
            'tags': 'Tags',
        }

class BlogReplyForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'style':'resize:none; outline:none;min-height:4rem',
                'class':'form-control no-border border-0',
                'placeholder':'Write a reply',
                'rows': 2,
                'cols': 50}))
    class Meta:
        model = BlogReply
        fields = ['content']
        
        
class CourseListForm(forms.ModelForm):
    
    title = forms.CharField(
		label='Title',
		max_length=1000,
		min_length=2,
		required=True,
  		validators=[alphanumeric_s],
		widget=forms.TextInput(
			attrs={
				"placeholder": "List Name",
				"class": "form-control"
			}
		)
	)
    
    year = forms.TypedChoiceField(
        coerce=int,
        choices=year_choices,
        initial=current_year,
        widget=forms.TextInput(
		    attrs={
				"placeholder": "Year",
				"class": "form-control"
			}
		)
    )
    
    error_css_class = "error"
    
    class Meta:
        model = CourseList
        fields=('title','year',)
        
        
class CourseListObjectsForm(forms.ModelForm):
    course_code = forms.CharField(
		label='',
		max_length=20,
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
		widget=forms.TextInput(
			attrs={
				"placeholder": "Instructor Lastname",
				"class": "form-control"
			}
		)
	)
    
    course_university = forms.ChoiceField(
		label='',
		required=True,
  		choices = UNIVERSITY_CHOICES,
  		widget=MySelect(
        attrs={
			"class":"form-control"
		}
        ), 
	)
    
    error_css_class = "error"
    
    class Meta:
        model = CourseListObjects
        fields=('course_code','course_university','course_instructor',)