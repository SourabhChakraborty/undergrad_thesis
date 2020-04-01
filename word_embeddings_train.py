import gensim
import re
import string
import json

with open('politics_tokens.json', 'r') as f:
    politics_tokens = json.load(f) 
    
model = gensim.models.Word2Vec(politics_tokens, size=100, window=10, min_count=10, workers=4)
model.save("politics_model1.model")