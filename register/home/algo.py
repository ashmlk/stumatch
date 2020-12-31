import string
import pytz
from dateutil import tz
from collections import Counter
from itertools import chain
import nltk
from nltk.collocations import *
from nltk.stem.porter import PorterStemmer
import string
import datetime
from math import log, sqrt
import json
from difflib import SequenceMatcher
import difflib

UNI_LIST = [
    "Acadia University",
    "Alberta University of the Arts",
    "Algoma University",
    "Athabasca University",
    "Atlantic School of Theology",
    "Bishop's University",
    "Booth University College",
    "Brandon University",
    "Brock University",
    "Canadian Mennonite University",
    "Cape Breton University",
    "Capilano University",
    "Carleton University",
    "Concordia University",
    "Crandall University",
    "Dalhousie University",
    "Emily Carr University of Art and Design",
    "Fairleigh Dickinson University",
    "Institut national de la recherche scientifique",
    "Kingswood University",
    "Kwantlen Polytechnic University",
    "Lakehead University",
    "Laurentian University",
    "MacEwan University",
    "McGill University",
    "McMaster University",
    "Memorial University of Newfoundland",
    "Mount Allison University",
    "Mount Royal University",
    "Mount Saint Vincent University",
    "New York Institute of Technology",
    "Niagara University",
    "Nipissing University",
    "Nova Scotia College of Art and Design University",
    "Ontario College of Art and Design University",
    "Ontario Tech University",
    "Queen's University at Kingston",
    "Quest University",
    "Redeemer University College",
    "Royal Military College of Canada",
    "Royal Roads University",
    "Ryerson University",
    "Saint Francis Xavier University",
    "Saint Mary's University",
    "Simon Fraser University",
    "St. Stephen's University",
    "St. Thomas University",
    "The King's University",
    "Thompson Rivers University",
    "Trent University",
    "Trinity Western University",
    "Tyndale University",
    "University Canada West",
    "University College of the North",
    "University of Alberta",
    "University of British Columbia",
    "University of Calgary",
    "University of Fredericton",
    "University of Guelph",
    "University of King's College",
    "University of Lethbridge",
    "University of Manitoba",
    "University of New Brunswick",
    "University of Northern British Columbia",
    "University of Ottawa",
    "University of Prince Edward Island",
    "University of Regina",
    "University of Saskatchewan",
    "University of Toronto",
    "University of Victoria",
    "University of Waterloo",
    "University of Western Ontario",
    "University of Windsor",
    "University of Winnipeg",
    "University of the Fraser Valley",
    "Université Laval",
    "Université Sainte-Anne",
    "Université de Moncton",
    "Université de Montréal",
    "Université de Sherbrooke",
    "Université de l'Ontario français",
    "Université du Québec en Abitibi-Témiscamingue",
    "Université du Québec en Outaouais",
    "Université du Québec à Chicoutimi",
    "Université du Québec à Montréal",
    "Université du Québec à Rimouski",
    "Université du Québec à Trois-Rivières",
    "Vancouver Island University",
    "Wilfrid Laurier University",
    "York University",
    "Yukon University",
    "École de technologie supérieure",
    "École nationale d'administration publique",
]

stop_words = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now",
]

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
porter = PorterStemmer()

epoch = datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)


def epoch_seconds(date):

    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(comments, likes):
    # comments recieve constant factor of 1.8
    return 1.8 * comments + likes


def top_score_posts(likes, comments):

    if (
        likes != 0 and comments != 0
    ):  # number of likes are usually higher than number on comment
        n = int(round((likes + comments) / (comments / likes)))
    else:
        n = (
            likes + comments
        )  # but still test both scenarios meaning sometimes comments will be more

    if n == 0:
        return 0

    z = 1.281551565545
    p = float(likes) / n

    left = p + 1 / (2 * n) * z * z
    right = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    under = 1 + 1 / n * z * z

    return (left - right) / under


def common_words(s):
    description = s.split()
    words = description
    most_common_words = [word for word, word_count in Counter(words).most_common(10)]
    return most_common_words


def _commonwords(text):

    tokens = nltk.wordpunct_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans("", "", string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if not w in stop_words]
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(3)
    phrases = finder.nbest(bigram_measures.pmi, 5)
    common_words = [word for word, word_count in Counter(words).most_common(10)]
    result = {
        "phrases": phrases,
        "common_words": common_words,
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

    if (likes != 0 or dislikes != 0) and (comments != 0 or wots != 0):
        n = int(
            round(
                ((likes - dislikes) + comments) / (wots + comments / (likes + dislikes))
            )
        )

    else:
        return 0

    z = 1.281551565545
    p = (float(likes - dislikes) * wots) / n

    left = p + 1 / (2 * n) * z * z
    right = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    under = 1 + 1 / n * z * z

    return (left - right) / under


def get_similar_university(name):

    return difflib.get_close_matches(name, UNI_LIST)[0]


def similar_string_ratio(a, b):

    return SequenceMatcher(None, a, b).ratio()


def get_uni_info(university):

    with open("static/jsons/world_universities_and_domains.json") as file:
        try:
            data = json.load(file)
            return next(
                item
                for item in data
                if similar_string_ratio(item["name"], university) > 0.9
            )
        except Exception as e:
            print(e)
            return None
