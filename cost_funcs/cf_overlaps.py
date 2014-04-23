from collections import Counter
from itertools import chain, combinations

import config

def times_each_group_sat_together(groups, group_size):
    """
    times_each_group_sat_together has the form [((id1, id2), count), ]
    """
    ids_by_group = []
    for group in groups:
        ids = [person.id for person in group.people]
        ids.sort()
        ids_by_group.append(ids)
    times_each_group_sat_together = (
        myCounter(chain.from_iterable(
            combinations(group, group_size) for group in ids_by_group)))
    return times_each_group_sat_together

def freqs(groups, group_size):
    freq_of_each_grouping = times_each_group_sat_together(groups, group_size)
    freq_of_freqs = myCounter(freq_of_each_grouping.values())
    return freq_of_freqs

def cost(freqs, group_size):
    cost = 0
    for freq, num_occurrences in freqs.iteritems():
        if freq != 1:
            cost += (freq**4 * num_occurrences)
    return cost

class myCounter(Counter):
    def __init__(self, iterable=None, **kwds):
        super(myCounter, self).__init__(iterable=iterable, **kwds)

