import os, django, random
from friendship.models import Friend, Follow, Block, FriendshipRequest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "register.settings")
django.setup()

from faker import Faker
from main.models import Profile
from home.models import Post, Blog, Buzz, Course, Comment, BuzzReply
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
import datetime
from notifications.signals import notify

def create_users(n):
    fake=Faker()
    for i in range(n):
        user = Profile.objects.create_user(username=fake.first_name()+"user"+str(i), email=fake.first_name()+fake.last_name()+"email"+str(i)+"@gmail.com", password="password"+fake.ean(length=13), university="Ryerson University")
        user.first_name=fake.first_name()
        user.last_name=fake.last_name()
        user.save()
    return "Success"

def create_bio():
    fake=Faker()
    for p in Profile.objects.all():
        bio=fake.sentence(nb_words=10)
        p.bio = bio
        p.save()
    return("success")

def create_posts(n):
    fake=Faker()
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    for i in range(n):
       id = random.choice(idl)
       title = fake.sentence()
       content = fake.paragraphs()
       post = Post.objects.create(title=title, content=content, author=Profile.objects.get(id=id))
       post.save()
       
def trim_posts():
    for p in Post.objects.all():
        p.content = p.content.rstrip("']")
        p.content = p.content.lstrip("['")
        p.content = p.content.replace("', '","")
        p.save()
        
def create_blogs(n):
    fake=Faker()
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    for i in range(n):
       id = random.choice(idl)
       title = fake.sentence(nb_words=3)
       pr = fake.paragraph(nb_sentences=30) 
       pr = pr.replace("']","")
       pr = pr.replace("['","")
       pr = pr.replace("', '","")
       blog = Blog.objects.create(title=title, content=pr, author=Profile.objects.get(id=id))
       blog.save()

def create_buzz(n):
    fake=Faker()
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    for i in range(n):
       id = random.choice(idl)
       nickname=fake.word()
       title = fake.sentence(nb_words=3)
       content = fake.sentence(nb_words=10)
       post = Buzz.objects.create(title=title, nickname=nickname, content=content, author=Profile.objects.get(id=id))
       post.save()
       
def add_tags_post():
    tags = ["love","instagood","photooftheday","fashion","beautiful","happy","cute","tbt","apple","like4like","followme","summer","girl","fun","travel","family","nature","smile","travel","nofilter","photography","smile","food","amazing","me"]
    for p in Post.objects.all():
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
    
def add_tags_buzz():
    tags = ["love","LOL","Command","adorable","lits","haha","groups","country","vacay","hot","instagood","photooftheday","fashion","beautiful","happy","cute","tbt","apple","like4like","followme","summer","girl","fun","travel","family","nature","smile","travel","nofilter","photography","smile","food","amazing","me"]
    for p in Buzz.objects.all():
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))

def add_tags_blog():
    tags = ["notice","posses","acidic","rotal","love","LOL","Command","adorable","lits","haha","groups","country","vacay","hot","instagood","photooftheday","fashion",\
        "beautiful","happy","cute","tbt","apple","like4like","followme","summer","girl","fun","travel","family","nature","smile","travel","nofilter","photography","smile","food","amazing","me"\
            "puppy","tech","asi","samsung","nrewtech","dopeness","weed","cheat","wipte","duck","phone","wipe","unruly","allways","everyday"]
    for p in Blog.objects.all():
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        p.tags.add(random.choice(tags))
        
def add_rand_likes():
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    for p in Post.objects.all():
        c = random.randint(7,36)
        ids = random.sample(idl,c)
        for i in ids:
            u = Profile.objects.get(id=i)
            p.likes.add(u)
    return("success")

def update_sv():
    Post.objects.all().update(sv=SearchVector('title','content'))
    Blog.objects.all().update(sv=SearchVector('title','content'))
    Buzz.objects.all().update(sv=SearchVector('title','content','nickname'))
    Course.objects.all().update(sv=SearchVector('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug'))
    Profile.objects.all().update(sv=SearchVector('username','first_name','last_name','university','program'))
    return "Success"

def create_friends():
    user = Profile.objects.get(username="squishy")
    idl = [31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    for i in idl:
        other_user = Profile.objects.get(pk=i)
        Friend.objects.add_friend(user,other_user,message='Hi! I would like to add you')
        fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
        fr.accept()
    return "success"

def create_mutual():
    id1 = [39 ,40, 41, 42 ,43 ,44 ,45, 46,47, 48 ,49, 50, 51, 52]
    id2= [ 53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 , 64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    
    for i in id1:
        user = Profile.objects.get(pk=i)
        for j in id2:
            other_user = Profile.objects.get(pk=j)
            Friend.objects.add_friend(user,other_user,message='Hi! I would like to add you')
            fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
            fr.accept()
    
    
def create_request():
    idlk = [9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28]     
    for k in idlk:
        print(k)
        user = Profile.objects.get(username="squishy")
        other_user = Profile.objects.get(pk=k)
        print(other_user)
        fr = Friend.objects.add_friend(other_user,user,message='Hi! I would like to add you')
    return "success"

def set_program():
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29]
    for i in idl:
        u = Profile.objects.get(id = i)
        u.program = "computer science"
        u.save()
    return "Success"

def create_comments():
    fake=Faker()
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    
    time_threshold = timezone.now() - datetime.timedelta(days=5)
    
    for p in Post.objects.filter(last_edited__gte=time_threshold):
        
        for i in range(random.randint(7,303)):
            profile = Profile.objects.get(id=random.choice(idl))
            c = fake.sentence(nb_words=6)
            comment = Comment.objects.create(post=p,name=profile,body=c)
            comment.save()
    return "Success"

def create_buzz_comments():
    fake=Faker()
    idl = [2,3, 4, 13 ,14, 15, 16, 17 ,18 ,19, 1 ,5, 6 ,7, 8 ,9 ,10 ,11 ,12 ,20 ,21 ,23 ,24 ,25 ,26 ,27, 28 ,29 ,30 ,31 ,32 ,33, 34 ,35, 36 ,37, 38, 39 ,40, 41, 42 ,43 ,44 ,45, 46, 47, 48 ,49, 50, 51, 52 ,53, 54, 55, 56, 57, 58, 59, 60 ,61 ,62, 63 ,\
        64 ,65, 66, 67 ,68, 69, 70, 71 ,72]
    
    for p in Buzz.objects.all():
        
        for i in range(random.randint(21,173)):
            profile = Profile.objects.get(id=random.choice(idl))
            c = fake.sentence(nb_words=4)
            n = fake.word()
            r = BuzzReply.objects.create(buzz=p,reply_author=profile,reply_nickname=n,reply_content=c)
            r.save()
    return "Success"

def update_posts():
    fake=Faker()
    for p in Post.objects.all():
        c = p.content
        cn = c + " " +  fake.word()
        p.content = cn
        p.save()
    return "success"        


def create_courses():
    
    codes = ['CPS109','HST543','ENG234','LST751','CPS209','CPS732','CPS821','POL209','POL902','POL532','ARB233','ABR432','TTL','CDF342','BIO9430','BIO489','CHM2434','CHE239','PHL8249','CPL3489','FSS290',\
        'FIN300','FIN234','GEO3490', 'GEO792','GEO2378','GEO2389','ITM130','ITM2390','TIY2849','ROL239','RIL3489','RMS349','RMG248','RMG348','POL781','CPS721','GEO123','GEO934','GEO607','HST901',\
            'RST349','GLS348','PSY833','PSY892','PSY389','PSY4489','CPS902']
    years = [2018,2019,2020]
    
    dif = [1,2,3,4]
    
    semester = [1,2,3,4]
    
    uni = ['Ryerson University','York University','University of Toronto']
    
    instructors = ['Jamson','Leonard','Adams','Smith','Taylor','Hemsworth','Evans','Nelson','Browns','Richardson','Andrews','Malik','Polsky','Reynolds Adamson','Trinter']
    
    for c in codes:
        
        for _ in range(3):
            i = random.choice(instructors)
            u = random.choice(uni)
            d = random.choice(dif)
            s = random.choice(semester)
            y = random.choice(years)
            
            course = Course.objects.create(course_code=c,course_instructor=i,course_university=u,course_difficulty=d,course_year=y,course_semester=s)
            
            course.save()
            
    return 'Success'

def add_courses():
    
    cc = Course.objects.all().count()
    
    for p in Profile.objects.all():
        random_id = random.sample(range(19,173),20) 
        for i in random_id:
            c = Course.objects.get(id=i)
            p.courses.add(c)
    return 'Success'

def delete_courses():
    
    for p in Profile.objects.all():
        
        for c in p.courses.all():
            p.courses.remove(c)
            
    return 'success'
    
            
            
def n():
    u = Profile.objects.get(username="starwars")
    users = Profile.objects.all()[:5]
    posts = Post.objects.filter(author=u)[:5]
    for p in posts:
        for i in users:
            p.likes.add(i)
    return "success"

def generate_comment_like_notifications():
    
    u = Profile.objects.get(username="starwars")
    posts = Post.objects.filter(author=u)[:5]
    comments = Comment.objects.filter(name=u,reply=None)[:15]
    users = Profile.objects.all()[:15]
    for (comment,user) in zip(comments,users):
        message = "CON_POST" + user.get_full_name() + " liked your comment on " + comment.post.author.get_full_name() + "'s post."
        description = comment.body
        notify.send(sender=user, recipient=comment.name, verb=message, description=description, target=comment.post, action_object=comment)
    return 'success'


def test_email():
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    from django.template.loader import render_to_string
    message = Mail(
        from_email='Corscope Team <no-reply@corscope.com>',
        to_emails='contact@corscope.com',
        subject='Welcome to Corscope',
        html_content = render_to_string('new_user_email.html', {'first_name': 'Arshia'})
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
        
