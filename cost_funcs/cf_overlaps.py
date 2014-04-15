from collections import Counter
from itertools import chain, combinations

import config

def display_output(freq_counter):
    for (k,v) in freq_counter.iteritems():
        if k != 1:
            print str(k) + ": " + str(v)


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
        Counter(chain.from_iterable(
            combinations(group, group_size) for group in ids_by_group)))
    return times_each_group_sat_together

def freqs(groups, group_size):
    freq_of_each_grouping = times_each_group_sat_together(groups, group_size)
    tally_of_freqs = []
    for grouping, freq in freq_of_each_grouping.iteritems():
        tally_of_freqs.append(freq)
    freq_of_freqs = Counter(tally_of_freqs)
    return freq_of_freqs

def cost(freqs, group_size):
    cost = 0
    for freq, num_occurrences in freqs.iteritems():
        if freq != 1:
            cost += (freq**4 * num_occurrences)

    if cost > 0 and config.verbose:
        print ''
        print "Number of times a group of " + str(group_size) + " sits together X times: "
        display_output(freqs)
        print "Cost of these overlaps: " + str(cost)
        print ''
    return cost
