import string
import pytz
from dateutil import tz
from collections import Counter
from itertools import chain
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import datetime
from math import log, sqrt
import json 
from difflib import SequenceMatcher

stop_words = stopwords.words('english')
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
porter = PorterStemmer()

epoch = datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)

def epoch_seconds(date):
    
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(comments, likes):
    # comments recieve constant factor of 1.8
    return  1.8 * comments + likes

def top_score_posts(likes, comments):
    
    if likes != 0 and comments != 0:   #number of likes are usually higher than number on comment
        n = int(round((likes + comments)/(comments/likes)))
    else:
        n = likes + comments  #but still test both scenarios meaning sometimes comments will be more

    if n == 0:
        return 0

    z = 1.281551565545
    p = float(likes) / n 

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

def common_words(s):
    description = s.split()
    words=description
    most_common_words= [word for word, word_count in Counter(words).most_common(10)]
    return most_common_words

def _commonwords(text):
    
    tokens = nltk.wordpunct_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if not w in stop_words]
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(3)
    phrases = finder.nbest(bigram_measures.pmi, 5)
    common_words = [word for word, word_count in Counter(words).most_common(10)]
    result = {
        "phrases":phrases,
        "common_words":common_words,
    }
    return result


def score_buzz(l, d):
    
    return l - d

def hot_buzz(likes, dislikes, wots, comments, date):
    
    s = score_buzz(likes, dislikes)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)


def top_buzz(likes, dislikes, wots, comments):
    
    if (likes != 0 or dislikes !=0) and (comments != 0 or wots != 0):   
        n = int(round(((likes-dislikes) + comments)/(wots+comments/(likes+dislikes))))

    else:
        return 0

    z = 1.281551565545
    p = (float(likes-dislikes) * wots) / n 

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

def similar_string_ratio(a, b):
    
    return SequenceMatcher(None, a, b).ratio()

def get_uni_info(university):
    
    with open('static/jsons/world_universities_and_domains.json') as file:
        data = json.load(file)
        return next(item for item in data if similar_string_ratio(item["name"], university) > 0.9)
        