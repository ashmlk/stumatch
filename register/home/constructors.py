import json
from home.models import Professors, Course
from django.contrib.postgres.search import SearchVector
from django.template.defaultfilters import slugify

def construct_professors():
    
    with open('static/jsons/profs.json') as f:
        data = json.load(f)
        for university in data[0]:
            for prof in data[0][university]:
                Professors.objects.create(university=university.lower(), first_name=prof['first_name'].lower(), last_name=prof['last_name'].lower())
                
        return "success"
    
def update_professors_index():
    
    search_vector = SearchVector('last_name', weight='A') +\
                     SearchVector('first_name', weight='B')
        
    for p in Professors.objects.all():
        
        p.sv = search_vector
        p.save()
    
    return "success"

# run third
def set_professors_slugs():
    
    for p in Professors.objects.all():
        p.name_slug = '-'.join((slugify(p.first_name.strip().lower()), slugify(p.last_name.strip().lower()))) 
        p.university_slug = slugify(p.university.strip().lower())
        p.save()
    return 'success'

# run second
def set_professor_courses():
    for c in Course.objects.all().order_by('course_university', 'course_instructor_fn', 'course_instructor','course_code').distinct('course_university', 'course_instructor_fn', 'course_instructor','course_code'):
        if Professors.objects.filter(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower()).exists():
            prof = Professors.objects.filter(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower()).first()
            prof.add_to_courses(c)
        else:
            Professors.objects.create(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower())
            prof = Professors.objects.get(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower())
            prof.add_to_courses(c)
    return 'success'

# run first
def update_professor_model():
    
    for c in Course.objects.order_by('course_university', 'course_instructor_fn', 'course_instructor').distinct('course_university', 'course_instructor_fn', 'course_instructor'):
        if not Professors.objects.filter(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower()).exists():
            Professors.objects.create(first_name=c.course_instructor_fn.lower(), last_name=c.course_instructor.lower(), university=c.course_university.lower())
    return 'success'
        