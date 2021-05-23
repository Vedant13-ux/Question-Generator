import numpy as np
import spacy
import re
import random
import nltk
from summarizer import Summarizer
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import uuid

def get_candidates(total_text,n_gram_range = (1, 1)):
    stop_words = "english"
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([total_text])
    candidates = count.get_feature_names()
    return candidates

def get_embeddings(text):
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding = model.encode([text])
    candidates = get_candidates(text)
    candidate_embeddings = model.encode(candidates)
    return candidate_embeddings, doc_embedding

def get_keywords(doc_embedding, candidate_embeddings,candidates, number_of_questions=10):
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    flattened_distances = [item for sublist in distances for item in sublist]
    flattened_distances = np.array(flattened_distances)
    keywords = [candidates[index] for index in flattened_distances.argsort()[-number_of_questions:]]
    return keywords 

def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    return sentences

def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences

def get_key_sentence_mapping(full_text, keywords, summarized_text):
    sentences = tokenize_sentences(full_text)
    filtered_keys=[]
    for keyword in keywords:
        if keyword.lower() in summarized_text.lower():
            filtered_keys.append(keyword)
    key_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
    return key_sentence_mapping

def generate_mcqs_fib(keyword_sentence_mapping, keywords, threshold = 0.5):
    mcq_dict = []
    fib_dict = []
    for index,key in enumerate(keyword_sentence_mapping):
        index = random.randint(0, len(keyword_sentence_mapping[key])-1 )
        sentence = keyword_sentence_mapping[key][index]
        pattern = re.compile(key, re.IGNORECASE)
        question = pattern.sub( " ____ ", sentence)
        options = []
        for i in range(3):
            options.append(random.choice(keywords))
        options.append(key)
        random.shuffle(options)
        random_choice = random.uniform(0, 1)
        if random_choice > threshold:
            mcq_dict.append({
                'id': str(uuid.uuid4()),
                'question':question,
                'type':'MCQ',
                'correct_answer':key,
                'options':options,
                'marked_answer':-1
            })
        else:
            fib_dict.append({
                'id': str(uuid.uuid4()),
                'question':question,
                'type':'FIB',
                'correct_answer':key,
                'marked_answer':-1
            })

    if len(fib_dict)!=0:
        mcq_dict.extend(fib_dict)
        return mcq_dict
    else:
        return mcq_dict

def generate_questions(text,number_of_questions,fib=False):
    candidates = get_candidates(text)
    candidate_embeddings, doc_embedding = get_embeddings(text)
    keywords = get_keywords(candidate_embeddings, doc_embedding, candidates, 2*int(number_of_questions))
    key_sentence_mapping = get_key_sentence_mapping(text, keywords,text)
    if fib:
        mcq_fib_questions = generate_mcqs_fib(key_sentence_mapping,keywords)
    else:
        mcq_fib_questions = generate_mcqs_fib(key_sentence_mapping,keywords,0)

    return mcq_fib_questions