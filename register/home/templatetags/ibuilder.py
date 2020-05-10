import string
import secrets
import random
from django import template

register = template.Library()

@register.simple_tag
def div_class():
    a = string.ascii_letters + string.digits
    p = ''.join(secrets.choice(a) for i in range(8))
    return p

@register.simple_tag(takes_context=True)
def check_is_liked(context):
    request = context['request']
    course = context['course']
    return course.is_liked(request.user)

@register.simple_tag(takes_context=True)
def check_not_liked(context):
    request = context['request']
    course = context['course']
    return course.not_liked(request.user)

@register.simple_tag
def bg_rand():
    bgs = ['#546e7a','#455a64','#90a4ae','#90a4ae','#616161','#fdd835','#00c853','#558b2f','#9ccc65','#43a047','#0091ea','#01579b','#2979ff','#512da8','#5c6bc0','#00c853','#1a237e','#ffbb33','#33b5e5',
           '#2BBBAD','#aa66cc','#ba68c8','#795548','#607d8b','#90a4ae','#007E33','#0d47a1','#4B515D','#3F729B','#c2185b','#880e4f','#7b1fa2','#4a148c','#1a237e','#00838f','#00b8d4','#00897b','#2e7d32','#f57f17','#5d4037']
    random.shuffle(bgs)
    return random.choice(bgs)


