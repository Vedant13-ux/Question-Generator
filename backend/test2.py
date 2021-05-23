import wikipedia
import spacy 
import pytextrank
import re
from  nltk.tokenize import sent_tokenize
text=wikipedia.page(title="Book").content
text=re.sub('\n|==|===', '', text)
sentences = [sent_tokenize(text)]
sentences = [y for x in sentences for y in x]
print(sentences)
# print(text)
# nlp = spacy.load('en_core_web_sm')
# nlp.add_pipe("textrank")
# doc=nlp(text)
# for sent in doc._.textrank.summary(limit_phrases=20, limit_sentences=5):
#     print(sent)