import enum
from PyDictionary import PyDictionary
from model import utils
import nltk
import uuid
import random


def get_glossary(text, number_of_words):
    glossary=[]
    dictionary=PyDictionary()
    keywords=utils.get_verbs(text)
    random.shuffle(keywords)
    keywords=keywords[:int(number_of_words/2)]
    keywords.extend(utils.get_nouns(text))
    random.shuffle(keywords)
    if(number_of_words<len(keywords)):
        keywords=keywords[:number_of_words]

    for word in keywords:
        meaning=dictionary.meaning(str(word))
        synonyms=dictionary.synonym(str(word))
        antonyms=dictionary.antonym(str(word))
        if meaning and synonyms and antonyms:
            glossary.append({
                'id':str(uuid.uuid4()),
                'word':str(word),
                'meaning':meaning,
                'synonyms':synonyms[:4],
                'antonyms':antonyms[:4]
            })
    return glossary

