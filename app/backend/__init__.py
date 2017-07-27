from nltk.stem.porter import PorterStemmer
import spacy
import itertools
import numpy as np

nlp = spacy.load('en')
stemmer = PorterStemmer()

LAW_COUNT = 705