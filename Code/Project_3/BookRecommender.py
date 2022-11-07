import pandas as pd
import numpy as np
import random
from ObjectToObjectRecommender import ObjectToObjectRecommender as OTO
from Data import patron_dfc as patron_df
from Data import inv_dfc as inv_df
import itertools


train_df = patron_df.head(len(patron_df) // 20)



iti = OTO(train_df, 'Patron_ID', 'Item_ID')
ptp = OTO(train_df, 'Item_ID', 'Patron_ID')


def get_patron_pairs(patron_id):
    pair_list = []

    # Get a list of pairs of patron, item that the patron has read.
    has_list = iti.objects_by_actor[patron_id]
    for item in has_list:
        pair_list.append([patron_id, item])

    has_len = len(pair_list)

    # Get a list of pairs of patron, item that the patron hasn't read.
    hasnt_list = random.sample([x for x in iti.object_ids if x not in has_list], has_len)

    for item in hasnt_list:
        pair_list.append([patron_id, item])

    return pair_list


def get_feat_vec(pair):
    feat_vec = []

    # User-Item pair (u, i)
    patron = pair[0]
    item = pair[1]

    # Popularity of i
    feat_vec.append(len(train_df[train_df['Item_ID'] == item]))

    # The similarity between i and the most similar book the user u has read
    max = 0
    items_read = iti.get_objects(patron)

    for item_id in items_read:
        sim_score = iti.jaccard(item, item_id)
        if sim_score > max:
            max = sim_score

    feat_vec.append(max)

    # The similarity between the user u and the most similar user who has read i
    max = 0
    patron_read = ptp.get_objects(item)

    for patron_id in patron_read:
        sim_score = ptp.jaccard(patron, patron_id)
        if sim_score > max:
            max = sim_score

    feat_vec.append(max)

    return feat_vec

pairs_lists = [get_patron_pairs(patron_id) for patron_id in iti.actor_ids]

pairs  = []
for pair_list in pairs_lists:
    for pair in pair_list:
        pairs.append(pair)


pair_feats = {str(pair): get_feat_vec(pair) for pair in pairs}

print(pair_feats)


# Popularity

# Jaccard Similarity

# User Similarity
