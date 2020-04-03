import gensim
import re
import string
import json

with open('stored_variables/politics_tokens_auth_sample.json', 'r') as f:
    politics_tokens = json.load(f) 
    
model = gensim.models.Word2Vec(politics_tokens, size=100, window=10, min_count=10, workers=4)
model.save("stored_variables/politics_model_user1.model")