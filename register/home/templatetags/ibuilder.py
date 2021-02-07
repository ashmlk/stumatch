import string
import secrets
import random
from django import template
from main.models import Profile, BookmarkBuzz, BookmarkBlog, BookmarkPost
from hashids import Hashids
import re, html
from register.mentions import extract

hashids = Hashids(salt="v2ga hoei232q3r prb23lqep weprhza9", min_length=8)

register = template.Library()


@register.simple_tag
def div_class():
    a = string.ascii_letters + string.digits
    p = "".join(secrets.choice(a) for i in range(8))
    return p


@register.simple_tag(takes_context=True)
def check_is_liked(context):
    request = context["request"]
    course = context["course"]
    return course.is_liked(request.user)


@register.simple_tag(takes_context=True)
def check_not_liked(context):
    request = context["request"]
    course = context["course"]
    return course.not_liked(request.user)


@register.simple_tag
def bg_rand():
    # bgs = ['#546e7a','#455a64','#90a4ae','#90a4ae','#616161','#fdd835','#00c853','#558b2f','#9ccc65','#43a047','#0091ea','#01579b','#2979ff','#512da8','#5c6bc0','#00c853','#1a237e','#ffbb33','#33b5e5',
    #'#2BBBAD','#aa66cc','#ba68c8','#795548','#607d8b','#90a4ae','#007E33','#0d47a1','#4B515D','#3F729B','#c2185b','#880e4f','#7b1fa2','#4a148c','#1a237e','#00838f','#00b8d4','#00897b','#2e7d32','#f57f17','#5d4037']
    bgs = [
        "#2b4a87",
        "#487BE0",
        "#487BE0",
        "#375fad",
        "#487BE0",
        "#375fad",
        "#2b4a87",
        "#487BE0",
        "#2b4a87",
        "#487BE0",
    ]
    random.shuffle(bgs)
    return random.choice(bgs)


@register.filter
def num_format(value):
    t = float("{:.3g}".format(int(value)))
    magnitude = 0
    while abs(t) >= 1000:
        magnitude += 1
        t /= 1000.0
    return "{}{}".format(
        "{:f}".format(t).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


@register.simple_tag(takes_context=True)
def is_bookmarked(context):
    request = context["request"]
    id = hashids.decode(context["hid"])[0]
    if context["t"] == "post":
        return BookmarkPost.objects.filter(
            user__id=request.user.id, obj__id=id
        ).exists()
    elif context["t"] == "blog":
        return BookmarkBlog.objects.filter(
            user__id=request.user.id, obj__id=id
        ).exists()
    elif context["t"] == "buzz":
        return BookmarkBuzz.objects.filter(
            user__id=request.user.id, obj__id=id
        ).exists()


@register.filter(name="get_dict_item")
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def mention_urlize(value):

    new_string = re.sub(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)", r'<a class="card-link" href="/u/\1">\g<0></a>', value)
    new_string = re.sub(r"(?:#)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)", r'<a class="card-link" href="/posts/tag/\1">\g<0></a>', value)
    return new_string
