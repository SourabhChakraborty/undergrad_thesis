import json
import pickle
from gensim.corpora import Dictionary
from scipy.sparse import csr_matrix, lil_matrix
import numpy as np

politics_dictionary = Dictionary.load("stored_variables/politics_dictionary_lda")

for i in range(24):
    print(i)
    curr_toks = []
    
    with open("stored_variables/politics_tokens2_month" + str(i) + ".json", 'r') as f:
        curr_toks = json.load(f)
    
    curr_bow = [politics_dictionary.doc2bow(doc) for doc in curr_toks]
    
    curr_mat = lil_matrix((len(curr_bow), len(politics_dictionary.id2token.keys())))
    
    for j in range(len(curr_bow)):
        for term, freq in curr_bow[j]:
            curr_mat[j,term] = freq
            
    curr_mat = csr_matrix(curr_mat)
                   
    with open("stored_variables/politics_all_tf" + str(i) + ".pickle", 'wb') as f:
        pickle.dump(curr_mat, f)
