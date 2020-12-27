from django import forms
from chat.models import Message
from django.db import models

class MessagePhotoForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('photo',) 