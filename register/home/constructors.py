import json
from home.models import Professors, Course, CourseObject, Review
from main.models import Profile
from django.contrib.postgres.search import SearchVector
from django.template.defaultfilters import slugify
import random
from faker import Faker
from helper.auto_find_courses import find_courses_and_profs

fake = Faker()


def construct_professors():

    with open("static/jsons/profs.json") as f:
        data = json.load(f)
        for university in data[0]:
            for prof in data[0][university]:
                Professors.objects.create(
                    university=university.lower(),
                    first_name=prof["first_name"].lower(),
                    last_name=prof["last_name"].lower(),
                )

        return "success"


def update_professors_index():

    search_vector = SearchVector("last_name", weight="A") + SearchVector(
        "first_name", weight="B"
    )

    for p in Professors.objects.all():

        p.sv = search_vector
        p.save()

    return "success"


# run third
def set_professors_slugs():

    for p in Professors.objects.all():
        p.name_slug = "-".join(
            (
                slugify(p.first_name.strip().lower()),
                slugify(p.last_name.strip().lower()),
            )
        )
        p.university_slug = slugify(p.university.strip().lower())
        p.save()
    return "success"


# run first
def update_professor_model():

    for c in Course.objects.order_by(
        "course_university", "course_instructor_fn", "course_instructor"
    ).distinct("course_university", "course_instructor_fn", "course_instructor"):
        if not Professors.objects.filter(
            first_name=c.course_instructor_fn.lower(),
            last_name=c.course_instructor.lower(),
            university=c.course_university.lower(),
        ).exists():
            Professors.objects.create(
                first_name=c.course_instructor_fn.lower(),
                last_name=c.course_instructor.lower(),
                university=c.course_university.lower(),
            )
    return "success"


def construct_courses(university=None):

    with open("static/jsons/courses.json") as f:
        data = json.load(f)
        if university == None:
            for university in data:
                for course in data[university]:
                    CourseObject.objects.create(
                        university=university, code=course.strip().replace(" ", "").upper(),
                    )
        else:
            for course in data[university]:
                CourseObject.objects.create(
                    university=university, code=course.strip().replace(" ", "").upper(),
                )

        return "success"


def create_random_review(code, uni):

    courses = Course.objects.filter(course_university__iexact=uni, course_code=code)
    for c in courses:
        rand = random.randint(0, Profile.objects.count() - 26)
        profiles = Profile.objects.all()[rand : rand + 25]
        for p in profiles:
            review = Review.objects.create(
                author=p,
                body=fake.paragraph(nb_sentences=3),
                year=random.randint(2016, 2021),
            )
            c.course_reviews.add(review)

    return "success"


def add_enrolled():

    for course in Course.objects.all():
        course_obj, cr = CourseObject.objects.get_or_create(
            code=course.course_code, university=course.course_university
        )
        profiles = course.profiles.all()
        for p in profiles:
            if p not in course_obj.enrolled.all():
                course_obj.enrolled.add(p)

    print("success")


def remove_professor_duplicates():
    for row in Professors.objects.all().reverse():
        if (
            Professors.objects.filter(
                first_name__iexact=row.first_name,
                last_name__iexact=row.last_name,
                university__iexact=row.university,
            ).count()
            > 1
        ):
            row.delete()
    return "success"


def remove_course_obj_duplicates():
    for row in CourseObject.objects.all().reverse():
        if (
            CourseObject.objects.filter(
                code__iexact=row.code, university__iexact=row.university
            ).count()
            > 1
        ):
            row.delete()
    return "success"


def clean_professors():
    for course in Course.objects.all():
        prof, cr = Professors.objects.get_or_create(
            first_name__iexact=course.course_instructor_fn,
            last_name__iexact=course.course_instructor,
            university__iexact=course.course_university,
        )
        c, cr2 = CourseObject.objects.get_or_create(
            code=course.course_code, university__iexact=course.course_university
        )
        prof.add_to_courses(c)
    return "success"

def create_prof_names_json(university=None):
    
    new_json = {}
    with open("static/jsons/profs.json") as f:
        data = json.load(f)
        for university in data[0]:
            new_json[university] = {}
            new_json[university]["first_names"] = []
            new_json[university]["last_names"] = []
            for prof in data[0][university]:
                first_name = prof["first_name"].split()
                for f in first_name:
                    new_json[university]["first_names"].append(f)
                new_json[university]["last_names"].append(prof["last_name"])
                
    with open('static/jsons/prof_names.json', 'w') as fp:
        json.dump(new_json, fp)
        
    return 'success'


def test_course_finder():
    t = """



    go to ...
    GO!
    Arshia Moslemian
    Search
    Shopping Cart
    Enroll/Drop/Swap
    My Academics
    My Class Schedule        |        Add        |        Drop        |        Swap        |        Term Information   
    My Class Schedule
    List View
    Weekly Schedule View
    Select Display Option
    L
    Winter 2021 | Undergraduate | Ryerson University
    Group Box
    Collapse section Class Schedule Filter Options Class Schedule Filter Options 
    Show Enrolled Classes
    Show Dropped Classes
    Show Waitlisted Classes
    BME 802 - Human-Computer Interaction
    Status  Units  Grading
    Enrolled
    1.00
    Graded
    Class Nbr  Section  Component  Days & Times  Room  Instructor  Start/End Date
    10910
    032
    Laboratory
    We 10:00AM - 12:00PM
    VIRTUAL Classroom
    Staff
    01/11/2021 - 04/16/2021
    10911
    031
    Lecture
    Th 9:00AM - 12:00PM
    VIRTUAL Classroom
    Kristiina McConville
    01/11/2021 - 04/16/2021
    BME 809 - Biomedical Systems Modelling
    Status  Units  Grading
    Enrolled
    1.00
    Graded
    Class Nbr  Section  Component  Days & Times  Room  Instructor  Start/End Date
    10941
    032
    Laboratory
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    01/18/2021 - 01/24/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    02/01/2021 - 02/07/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    02/22/2021 - 02/28/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    03/08/2021 - 03/14/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    03/22/2021 - 03/28/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    04/05/2021 - 04/11/2021
    10942
    031
    Lecture
    Tu 9:00AM - 12:00PM
    VIRTUAL Classroom
    Dafna Sussman
    01/11/2021 - 04/16/2021
    10943
    033
    Tutorial
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    01/11/2021 - 01/17/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    01/25/2021 - 01/31/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    02/08/2021 - 02/12/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    03/01/2021 - 03/07/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    03/15/2021 - 03/21/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    03/29/2021 - 04/04/2021
    
    
    
    Tu 4:00PM - 6:00PM
    VIRTUAL Classroom
    Staff
    04/12/2021 - 04/16/2021
    BME 872 - Biomedical Image Analysis
    Status  Units  Grading
    Enrolled
    1.00
    Graded
    Class Nbr  Section  Component  Days & Times  Room  Instructor  Start/End Date
    10950
    011
    Lecture
    Mo 2:00PM - 5:00PM
    VIRTUAL Classroom
    April Khademi
    01/11/2021 - 04/16/2021
    10951
    012
    Laboratory
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    01/18/2021 - 01/24/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    02/01/2021 - 02/07/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    02/22/2021 - 02/28/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    03/08/2021 - 03/14/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    03/22/2021 - 03/28/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    04/05/2021 - 04/11/2021
    10952
    013
    Tutorial
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    01/11/2021 - 01/17/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    01/25/2021 - 01/31/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    02/08/2021 - 02/12/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    03/01/2021 - 03/07/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    03/15/2021 - 03/21/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    03/29/2021 - 04/04/2021
    
    
    
    Mo 8:00AM - 10:00AM
    VIRTUAL Classroom
    Staff
    04/12/2021 - 04/16/2021
    CEN 800 - Law and Ethics in Eng Practice
    Status  Units  Grading
    Enrolled
    1.00
    Graded
    Class Nbr  Section  Component  Days & Times  Room  Instructor  Start/End Date
    12618
    021
    Lecture
    Tu 1:00PM - 4:00PM
    VIRTUAL Classroom
    Vincent Chan
    01/11/2021 - 04/16/2021
    MTH 410 - Statistics
    Status  Units  Grading
    Enrolled
    1.00
    Graded
    Class Nbr  Section  Component  Days & Times  Room  Instructor  Start/End Date
    11808
    072
    Laboratory
    We 2:00PM - 3:00PM
    VIRTUAL Classroom
    Staff
    01/11/2021 - 04/16/2021
    11809
    071
    Lecture
    Fr 1:00PM - 2:00PM
    VIRTUAL Classroom
    Leul Fisseha
    01/11/2021 - 04/16/2021
    
    
    
    We 8:00AM - 10:00AM
    VIRTUAL Classroom
    Leul Fisseha
    01/11/2021 - 04/16/2021
    Printer Friendly Page
    Go to top iconGo to top

    """
    u = "Ryerson University"
    f= "Arshia"
    l = "Moslemian"
    r = find_courses_and_profs(text=t, university=u, first_name=f, last_name=l)
    print(r)
    return True