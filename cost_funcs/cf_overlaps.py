from collections import Counter
from itertools import chain, combinations
import numpy as np

import config

def initialize_ids_matrix(num_ids, group_size):
    if group_size == 2:
        ids_matrix = np.zeros((num_ids, num_ids), dtype=np.int)
    elif group_size == 3:
        ids_matrix = np.zeros((num_ids, num_ids, num_ids), dtype=np.int)
    else:
        raise SyntaxError("Currently, Grouper can only calculate the frequencies " + \
                          "of groups of 2 or 3")
    return ids_matrix

def update_ids_matrix(ids_matrix, people_tuple, group_size):
    if group_size == 2:
        ids_matrix[people_tuple[0]][people_tuple[1]] += 1
    elif group_size == 3:
        ids_matrix[people_tuple[0]][people_tuple[1]][people_tuple[2]] += 1

def create_freqs_matrix(groups, num_people, group_size):
    ids_matrix = initialize_ids_matrix(num_people, group_size)
    for group in groups:
        ids = [person.id for person in group.people]
        ids.sort()
        overlaps = combinations(ids, group_size)
        for grouping in overlaps:
            update_ids_matrix(ids_matrix, grouping, group_size)
    return ids_matrix

def freqs(ids_matrix):
    flattened_matrix = [x for x in ids_matrix.flat if x != 0]
    freqs = Counter(flattened_matrix)
    return freqs

def cost(freqs, group_size):
    cost = 0
    for freq, num_occurrences in freqs.iteritems():
        if freq != 1:
            cost += (freq**4 * num_occurrences)
    return cost
