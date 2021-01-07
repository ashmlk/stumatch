from main.models import Profile
import random

def get_max_username_length():
   from register.settings.common import USERNAME_MAX_LENGTH 
   return USERNAME_MAX_LENGTH


def get_usernames():
    
    usernames = set(
        list(
            Profile.objects.all().values_list("username", flat=True)
        )
    )
    return usernames

def generate_username(first, last, email):
    
    USERNAMES = get_usernames()
    accepted_chars = ['_','.']
    
    first = first.replace(' ','').lower()
    last = last.replace(' ','').lower()
    
    last_length = len(last)
    min_last_length = 2 if last_length > 1 else 1

    email_without_domain = email[:email.find("@")]
    email_without_domain = email_without_domain.replace("-","_").lower().strip()[:get_max_username_length()].replace(' ','')
    
    if email_without_domain not in USERNAMES:
        return email_without_domain
    
    else:
        username = email_without_domain
        counter = 0
        
        while username in USERNAMES and counter < 75:
            last_index = random.randint(min_last_length,last_length-1)
            last_name = last[:last_index]
            random_chars = random.choice(accepted_chars)
            l = [last_name, first, random_chars]
            print(l)
            random.shuffle(l)
            print(l)
            username = "".join(l).replace(' ','').lower()
            counter += 1
        
        if username not in USERNAMES and not Profile.objects.filter(username=username).exists():
            return username
        
        counter = 0
        
        while username in USERNAMES and counter < 150:
            rand = random.getrandbits(64)
            username = email_without_domain + str(random)
            counter += 1
            
        if username not in USERNAMES and not Profile.objects.filter(username=username).exists():
            return username
        
        while username in USERNAMES:
            rand = random.getrandbits(92)
            last_index = random.randint(min_last_length,last_length-1)
            last_name = last[:last_index]
            username = str((first + last_name) + str(rand)).lower().replace(' ','')
            
        return username
            
def get_first_last_name(full_name):
    
    first_name = last_name = None
    full_name = full_name.strip().split()
    len_name = len(full_name)
    if len_name == 1:
        first_name = full_name
    elif len_name == 3:
        first_name = full_name[0] + " " + full_name[1]
        last_name = full_name[2]
    elif len_name >= 4:
        first_name = " ".join(full_name[:2])
        last_name = " ".join(full_name[2:])
        
    return first_name, last_name
    