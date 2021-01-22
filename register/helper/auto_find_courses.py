from home.models import Professors
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When

import nltk, spacy, json, string, re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from spacy import displacy
from collections import Counter, OrderedDict 
from nltk.corpus import stopwords, words, wordnet
from nameparser.parser import HumanName
from itertools import chain

stop_words = stopwords.words('english')
english_words = set(words.words())

def get_uni_regex_common_words(university): 
    with open("static/jsons/find_courses.json") as f:
        data = json.load(f)
        data = data[university]
        uni_courses_regex = data["regex"]
        uni_courses_regex_list = data["regex_list"]
        common_words = data["common_words"]
        prof_order = data["prof_order"]
        prof_name_order = data["prof_name_order"]
        f.close()
    return uni_courses_regex, uni_courses_regex_list, common_words, prof_order, prof_name_order
        
def get_prof_names(university):
    with open("static/jsons/prof_names.json") as f:
        data = json.load(f)
        first_names = data[university.lower()]['first_names']
        last_names = data[university.lower()]['last_names']
        f.close()
    return set(first_names), set(last_names)

def get_instructors(university, instructors, num):
    
    num_pairs = num # number of pairs means firstname and lastnames
    p = index = complete_pairs = 0
    instructor_pairs = {}
    professors = Professors.objects.filter(university__iexact=university)
    for _ in range(len(instructors)):
        if complete_pairs == num_pairs:
            break
        if index + 1 <= len(instructors) - 1:
            first_name = instructors[index]
            last_name = instructors[index+1]
            if professors.filter(first_name__iexact=first_name, last_name__iexact=last_name).exists():
                prof = professors.filter(first_name__iexact=first_name, last_name__iexact=last_name).first()
                instructor_pairs[p] = {
                    "first":prof.first_name.capitalize(),
                    "last":prof.last_name.capitalize(),
                }
                index += 2
                p += 1
                complete_pairs += 1
            else:
                instructor_pairs[p] = {
                    "first":first_name,
                    "last":'N/A',
                }
                index += 1
                p += 1
        
    if p > num_pairs:
        c = 0
        remove_indices = []
        for p in instructor_pairs:
            if instructor_pairs[p]["last"] == 'N/A':
                if c >= 1 or instructor_pairs[p]["first"].lower() in english_words:
                    remove_indices.append(p)
                c+= 1
    instructors = {}
    for i in remove_indices:
        del instructor_pairs[i]   
    for i, p in enumerate(instructor_pairs):
        instructors[i] = instructor_pairs[p]
    return instructors

def find_courses_and_profs(text, university, first_name=None, last_name=None):
    text = text.replace(first_name,'')
    text = text.replace(last_name,'')
    days = ['Sun','Sunday','Mon', 'Monday','Tue','Tuesday', 'Wed', 'Wednesday','Thurs','Thursday','Fri','Friday','Sat','Saturday','Su','Mo','Tu','We','Th','Fr','Sa']
    uni_courses_regex, uni_courses_regex_list, UniCommonWords, prof_order, prof_name_order = get_uni_regex_common_words(university=university)
    prof_first_names, prof_last_names = get_prof_names(university)
    r = re.compile(uni_courses_regex_list)
    table = str.maketrans(dict.fromkeys(string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(uni_courses_regex, '\\1\\2\\3', text)
    words = word_tokenize(text)
    words = filter(lambda ThisWord: not (re.match('^(?:(?:[0-9]{2}[:\/,]){2}[0-9]{2,4}|am|pm|PM|AM)$', ThisWord) or re.match(r'^\d+(?:(?:\.|:\d+)[ ]*(?:am|AM|pm|PM)?|(?:am|AM|pm|PM))(?:[ ]*-[ ]*\d+(?:(?:\.|:\d+)[ ]*(?:am|AM|pm|PM)?|(?:am|AM|pm|PM)))*$', ThisWord )), words)

    excluded_set = set(chain(stop_words, map(str.lower, UniCommonWords)))
    text_f = " ".join(list(words))
    text_f = text_f.translate(table)
    text_f = text_f.split()
    filtered_words = []
    for word in text_f:
        words = str(word)
        if (word.lower().strip() in map(str.lower, prof_first_names)) or (word.lower().strip() in map(str.lower, prof_last_names)) or (re.match(uni_courses_regex_list, word.strip()) is not None):
            filtered_words.append(word)    
    filtered_words = [w for w in filtered_words if w.lower() not in excluded_set]
    text_f = " ".join(filtered_words).translate(table)
    text_f = re.sub(r"$\d+\W+|\b\d+\b|\W+\d+$", " ", text_f)
    text_f = re.sub(r'\s+', ' ', text_f)
    text_f = list(OrderedDict.fromkeys(text_f.split()))
    courses = list(filter(r.match, text_f))
    instructors = [x for x in text_f if x not in courses]
    instructors = get_instructors(university, instructors, len(courses))
    result = {}
    if prof_name_order == "fl":
        for i, c in enumerate(courses):
            course_pair = {}
            course_pair["code"] = c
            course_pair["instructor_first_name"] = instructors[i]["first"]
            course_pair["instructor_last_name"] =  instructors[i]["last"]
            result[f'course_{i}'] = course_pair
    elif prof_name_order == 'lf':
        for i, c in enumerate(courses):
            course_pair = {}
            course_pair["code"] = courses[i]
            course_pair["instructor_first_name"] = f
            course_pair["instructor_last_name"] = l
            result[f'pair_{i}'] = course_pair
            
    result = json.dumps(result)
    print(result)
    return result
    
  