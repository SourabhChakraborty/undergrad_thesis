import json
from gensim.models import LdaModel
from gensim.corpora import Dictionary

with open('politics_tokens.json', 'r') as f:
    politics_tokens = json.load(f) 
    
politics_dictionary = Dictionary.load("politics_dictionary_lda")

politics_corpus = [politics_dictionary.doc2bow(text) for text in politics_tokens]

for i in range(10, 51):
    print(i)
    politics_ldamodel = LdaModel(politics_corpus, num_topics = i, id2word = politics_dictionary)
    filename = "lda_models/politics_lda" + str(i) + ".model"
    politics_ldamodel.save(filename)