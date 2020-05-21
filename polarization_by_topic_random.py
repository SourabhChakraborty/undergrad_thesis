import json
import pickle
from gensim.corpora import Dictionary

from scipy.sparse import coo_matrix, csr_matrix, lil_matrix, csc_matrix, diags, vstack

import numpy as np
import random

politics_dictionary = Dictionary.load("stored_variables/politics_dictionary_lda")

sanders_tf_by_month = []
trump_tf_by_month = []

for i in range(24):        
    with open("stored_variables/politics_sanders_tf" + str(i) + ".pickle", 'rb') as f:
        sanders_tf_by_month.append(pickle.load(f))
        
    with open("stored_variables/politics_trump_tf" + str(i) + ".pickle", 'rb') as f:
        trump_tf_by_month.append(pickle.load(f))


trump_words = ['donald','trump','drumpf']
sanders_words = ['bernie','sanders','sander']
clinton_words = ['hillary','hilary','clinton','hrc']

immigration_words = ['immigrant','immigrants', 'immigration', 
                     'illegals', 'aliens', 'mexican', 'mexicans', 
                     'undocumented', 'amnesty', 'deportation', 
                     'deporting', 'visas', 'migrants', 'visa', 
                     'border', 'deportations', 'h1b', 'alien', 
                     'foreigners', 'mexico', 'overstayed', 
                     'muslims', 'overstaying', 'crossings', 
                     'citizenship', 'assimilation', 'migration', 
                     'immigrating', 'natives', 'overstay', 'muslim', 
                     'deport', 'refugees', 'refugee', 'deports', 
                     'deported', 'cubans', 'immigrate', 
                     'latinos', 'hispanics', 'entering', 
                     'asians', 'migrant']

healthcare_words = ['healthcare','health','medicare','insurance',
                   'medicaid', 'uninsured', 'deductibles', 'insurers', 
                    'copays', 'hmo', 'reimbursements', 'insurances', 
                    'premiums', 'insured', 'dental', 'reimbursement', 
                    'nhs', 'supplemental', 'preventative', 'hospitals', 
                    'obamacare', 'insurer', 'medical', 'overhead', 
                    'aca','checkups', 'enrollees', 
                    'patients', 'socialized', 'prescriptions', 'wellness', 
                    'medicine', 'physicians', 'heathcare', 'deductible', 
                    'preventive', 'medication', 'medicade', 'heath']

campaign_words = ["campaign","election", "elections", "campaigns", "vote", "voting", 
                  'primary', 'primaries', 'votes', 'candidate', 'challengers', 'caucus', 
                  'incumbents', 'candidates', 'voters', 'challenger', 'nomination', 'nominee', 
                  'party', 'caucuses', 'ballot', 'dnc', 'superdelegates',  
                  'independents', 'endorsements', 'campaigning', 'reelection', 'dems', 
                  'fundraising', 'voter', 'contests', 'november', 'electorate', 'debates', 
                  'incumbent', 'enthusiasm', 'presidency', 'midterm', 'contest', 
                  'ticket', 'democrats', 'turnout', 'midterms']

gun_words = ['handguns', 'handgun', 'concealed', 'ccw', 'weapon', 
             'rifles', 'pistols', 'suppressors', 'ammunition', 'automatics',
             'atf', 'silencers', 'ammo', 'hunters', 'robberies', 'pistol', 
             'lethal', 'rifle', 'shotguns', 'homicides', 'shooters', 
             'suppressor', 'ar15s', 'homicide', 'fingerprint', 'weapons', 
             'hunting', 'knives', 'buyback', 'ffls', 'explosives']

def subset_with_words(mat, word_list):
    idx_list = [politics_dictionary.token2id[word] for word in word_list]
    
    user_ids = np.nonzero(mat[:,idx_list].sum(axis=1))[0]
    
    return mat[user_ids, :]

word_sets = [trump_words, sanders_words, clinton_words, immigration_words, healthcare_words, campaign_words, gun_words]

sanders_tf_subsets = []
trump_tf_subsets = []

for i in range(len(sanders_tf_by_month)):
    curr_sanders_subsets = []
    curr_trump_subsets = []
    
    for ws in word_sets:
        curr_sanders_subsets.append(subset_with_words(sanders_tf_by_month[i], ws))
        curr_trump_subsets.append(subset_with_words(trump_tf_by_month[i], ws))
        
    sanders_tf_subsets.append(curr_sanders_subsets)
    trump_tf_subsets.append(curr_trump_subsets)
    
# from https://github.com/ddemszky/framing-twitter/blob/master/3_polarization_measures/calculate_polarization_simple.py
def get_party_q(party_counts, exclude_user_id = -1):
    user_sum = party_counts.sum(axis=0)
    if exclude_user_id > -1:
        user_sum -= party_counts[exclude_user_id, :]
    total_sum = user_sum.sum()
    return user_sum / total_sum

def get_rho(dem_q, rep_q):
    denom = dem_q + rep_q
    denom[denom == 0] = 1
    return (rep_q / (denom)).transpose()

def calculate_polarization(dem_counts, rep_counts, sample_size = 1000):
    dem_no = dem_counts.shape[0]
    rep_no = rep_counts.shape[0]
    
    if sample_size < dem_no:
        dem_indices = random.sample(range(dem_no), sample_size)
        dem_counts = dem_counts[dem_indices, :]
        dem_no = sample_size
        
    if sample_size < rep_no:
        rep_indices = random.sample(range(rep_no), sample_size)
        rep_counts = rep_counts[rep_indices, :]
        rep_no = sample_size
        
    
    dem_user_total = dem_counts.sum(axis=1)
    rep_user_total = rep_counts.sum(axis=1)
    
    # equivalent to dem_counts / dem_user_total
    dem_user_distr = (diags(1 / dem_user_total.A.ravel())).dot(dem_counts)  # get row-wise distributions
    rep_user_distr = (diags(1 / rep_user_total.A.ravel())).dot(rep_counts)
    assert (set(dem_user_total.nonzero()[0]) == set(range(dem_no)))  # make sure there are no zero rows
    assert (set(rep_user_total.nonzero()[0]) == set(range(rep_no)))  # make sure there are no zero rows

    dem_q = get_party_q(dem_counts)
    rep_q = get_party_q(rep_counts)

    # apply measures via leave-out
    dem_addup = 0
    rep_addup = 0
    
    for i in range(dem_no):
        dem_leaveout_q = get_party_q(dem_counts, i)
        token_scores_dem = 1. - get_rho(dem_leaveout_q, rep_q)
        dem_addup += dem_user_distr[i, :].dot(token_scores_dem)[0, 0]
    
    for i in range(rep_no):
        rep_leaveout_q = get_party_q(rep_counts, i)
        token_scores_rep = get_rho(dem_q, rep_leaveout_q)
        rep_addup += rep_user_distr[i, :].dot(token_scores_rep)[0, 0]
    rep_val = 1 / rep_no * rep_addup
    dem_val = 1 / dem_no * dem_addup
    return 1/2 * (dem_val + rep_val)

def pi_val_confidence_interval(lst, estimate, t_k = 50, t_full = 5000):
    assert(len(lst) == 100)
    
    pi_k_lst = sorted(lst)
    pi_avg = np.mean(pi_k_lst)
    q_k = [np.sqrt(t_k) * (pi_k - pi_avg) for pi_k in pi_k_lst]
    
    return (estimate - q_k[89] / np.sqrt(t_full), estimate - q_k[10] / np.sqrt(t_full))

pi_vals_random = []
pi_vals_random_ci_below = []
pi_vals_random_ci_above = []

for i in range(24):
    print(i)
    pi_vals_curr = []
    pi_vals_ci_below_curr = []
    pi_vals_ci_above_curr = []
    
    for j in range(len(word_sets)):
        sanders_mat_original = sanders_tf_subsets[i][j][sanders_tf_subsets[i][j].sum(axis=1).nonzero()[0],:]
        trump_mat_original = trump_tf_subsets[i][j][trump_tf_subsets[i][j].sum(axis=1).nonzero()[0],:]
        
        joint_mat = vstack([sanders_mat_original, trump_mat_original])
            
        sanders_random = random.sample(list(range(joint_mat.shape[0])), sanders_mat_original.shape[0])
        trump_random = list(set(range(joint_mat.shape[0])).difference(sanders_random))
        
        sanders_mat = joint_mat[sanders_random,:]
        trump_mat = joint_mat[trump_random,:]

        pi = calculate_polarization(sanders_mat, trump_mat, sample_size=5000)

        pi_vals_curr.append(pi)

        subsample = []

        for _ in range(100):
            subsample.append(calculate_polarization(sanders_mat, trump_mat, sample_size=50))
        
        below, above = pi_val_confidence_interval(subsample, pi, t_k=50, t_full=5000)
        
        pi_vals_ci_below_curr.append(below)
        pi_vals_ci_above_curr.append(above)
        
    pi_vals_random.append(pi_vals_curr)
    pi_vals_random_ci_below.append(pi_vals_ci_below_curr)
    pi_vals_random_ci_above.append(pi_vals_ci_above_curr)
    
    with open("stored_variables/pi_vals_random_topic.pickle", 'wb') as f:
        pickle.dump(pi_vals_random, f)
        
    with open("stored_variables/pi_vals_random_topic_ci_below.pickle", 'wb') as f:
            pickle.dump(pi_vals_random_ci_below, f)

    with open("stored_variables/pi_vals_random_topic_ci_above.pickle", 'wb') as f:
            pickle.dump(pi_vals_random_ci_above, f)