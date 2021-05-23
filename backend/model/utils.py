import spacy 
from nltk.corpus import wordnet

nlp = spacy.load('en_core_web_sm')

def get_proper_nouns(text):
    doc = nlp(text)
    proper_nouns = []
    for ent in doc:
        if ent.pos_ == 'PROPN':
            proper_nouns.append(ent)
    return list(set(proper_nouns))

def get_nouns(text):
    nouns = []
    doc = nlp(text)
    nouns = [ent.lemma_ for ent in doc if ent.pos_ == 'NOUN']
    return list(set(nouns))

def get_verbs(text):
    doc = nlp(text)
    verbs = [ent.lemma_ for ent in doc if ent.pos_ == 'VERB']
    return list(set(verbs))

def get_numbers(text):
    numbers = []
    doc = nlp(text)
    for ent in doc:
        if ent.pos_ == 'NUM':
            numbers.append(ent)
    return list(set(numbers))

def create_opposite_word(word):
    antonyms = []
    word = str(word).lower()
    syns = wordnet.synsets(str(word))
    if syns:
        for l in syns[0].lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())    
    return antonyms

def get_sentence_properties(sentence):
    doc = nlp(sentence)
    sentence = list(doc.sents)[0]
    root_word = sentence.root 
    proper_nouns = []
    nouns = []
    adjectives = []
    numbers = []
    for ent in doc:
        if ent.pos_ == 'PROPN':
            proper_nouns.append(ent)
        elif ent.pos_ == 'NUM':
            numbers.append(ent)
        elif ent.pos_ == 'NOUN':
            nouns.append(ent)
        elif ent.pos_ == "ADJ":
            adjectives.append(ent)
        
    return {
        'root_word':root_word,
        'adjectives':adjectives,
        'proper_nouns':proper_nouns,
        'number':numbers,
        'nouns':nouns,
        'adjectives':adjectives
    }
        

