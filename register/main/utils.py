from main.models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import re

USERNAME_REGEX = r"^(?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9._ ]+$"

def validate_username_regex(val):
    
    if re.match(USERNAME_REGEX, val):
        return True
    else:
        return False   
    
def check_username_acceptable(val):
    
    data = dict()
    valid = validate_username_regex(val)
    data['valid_status'] = valid
    if valid:
        if Profile.objects.filter(username=val).exists():
            data['errors'] = True
            data['error_message'] = 'This username already exists. Please try another.'
            return data
        else:
            data['errors'] = False
            return data
    else:
        data['errors'] = True
        data['error_message'] = 'Invalid username. Please try another.' 
        return data
    
def check_email_acceptable(val):
    data = dict()
    try:
        validate_email(val)
    except ValidationError:
        data['errors'] = True
        data['error_message'] = 'Email address is inavalid. Please try again.'
        return data
    else:
        if Profile.objects.filter(email__iexact=val).exists():
            data['errors'] = True
            data['error_message'] = 'Email address is inavalid. Please try again.'
            return data
        else:
            data['errors'] = False
            return data