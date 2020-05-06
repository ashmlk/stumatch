import string
import secrets
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

