from nltk import sent_tokenize, word_tokenize
from model import utils
import random
from PyDictionary import PyDictionary
import uuid

def question_json(sentence, correct_word, wrong_word):
    choice = random.choice((0,1))
    if choice>0.5 :
        return {
                    'id':str(uuid.uuid4()),
                    'question':sentence,
                    'type':'TOF',
                    'options':["True","False"], 
                    'correct_answer':"True",
                    'marked_answer':-1
                }
    else:
        index_correct=sentence.find(str(correct_word))
        wrong_sentence=sentence[:index_correct]+ str(wrong_word) + sentence[index_correct+ len(str(wrong_word)): ]
        return {
                    'id':str(uuid.uuid4()),
                    'question':wrong_sentence,
                    'type':'TOF',
                    'options':["True","False"], 
                    'correct_answer':"False",
                    'marked_answer':-1
                }

    


def generate_true_false(text, number_of_questions=5):
    paragraph_proper_nouns, paragraph_nouns, paragraph_numbers = utils.get_proper_nouns(text), utils.get_nouns(text), utils.get_numbers(text)
    sentences = sent_tokenize(text)
    true_or_false_questions = []
    for sentence in sentences:
        sentence_properties = utils.get_sentence_properties(sentence)
        antonyms = utils.create_opposite_word(sentence_properties['root_word'])
        if antonyms:
            true_or_false_questions.append(question_json(sentence,sentence_properties['root_word'],antonyms[0]))
        elif sentence_properties['proper_nouns']:
            chosen_proper_noun = random.choice(paragraph_proper_nouns)
            sentence_proper_noun = random.choice(sentence_properties['proper_nouns'])
            true_or_false_questions.append(question_json(sentence,sentence_proper_noun,chosen_proper_noun)) 
        elif sentence_properties['number']:
            chosen_number = random.choice(paragraph_numbers)
            sentence_number = random.choice(sentence_properties['number'])
            true_or_false_questions.append(question_json(sentence,sentence_number,chosen_number)) 
        else:
            random_choice = random.choice((0,1))
            if random_choice > 0.5:
                true_or_false_questions.append({
                    'id':str(uuid.uuid4()),
                    'question':sentence,
                    'type':'TOF',
                    'options':["True","False"], 
                    'correct_answer':"True",
                    'marked_answer':-1
                })
    
    if len(true_or_false_questions) < number_of_questions:
        return true_or_false_questions

    return true_or_false_questions[:number_of_questions]