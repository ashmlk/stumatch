import json
from home.models import Professors
from django.contrib.postgres.search import SearchVector

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
        