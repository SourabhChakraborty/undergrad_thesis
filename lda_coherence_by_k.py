import json
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel

from matplotlib import pyplot as plt

with open('politics_tokens.json', 'r') as f:
    politics_tokens = json.load(f) 
    
politics_dictionary = Dictionary.load("politics_dictionary_lda")

politics_corpus = [politics_dictionary.doc2bow(text) for text in politics_tokens]

coherence_models = []
coherence_values = []
k_values = list(range(10, 51))

for k in k_values:
    print(k)
    filename = 'lda_models/politics_lda' + str(k) + '.model'
    curr_lda_model = LdaModel.load(filename)
    curr_coherence_model = CoherenceModel(model = curr_lda_model, corpus = politics_corpus, coherence = 'u_mass')
    coherence_values.append(curr_coherence_model.get_coherence())
    coherence_models.append(curr_coherence_model)
    
with open('lda_coherence_vals.json', 'w') as f:
    json.dump(coherence_values, f)