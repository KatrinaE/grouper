from collections import Counter

import config

def freqs(groups):
    all_people_ever_at_groups = {}
    for group in [group for group in groups]:
        ids = [person.id for person in group.people]
        try:
            all_people_ever_at_groups[group.name].extend(ids)
        except KeyError: # group not yet in dict
            all_people_ever_at_groups[group.name] = ids

    frequencies = []
    for group_name, ids in all_people_ever_at_groups.iteritems():
        c = Counter(ids)
        frequencies.extend(c.values())
    frequencies_counter = Counter(frequencies)
    return frequencies_counter

def cost(frequencies_counter):
    cost = 0
    for freq, tally in frequencies_counter.iteritems():
        if freq > 1:
            cost += (freq**4 * tally)
            if config.verbose:
                print str(tally) + " people sit in the same spot " + str(freq) + " times."
    return cost


def cf_same_spot(groups):
    """ Cost of people sitting in same place multiple times """
    frequencies_counter = freqs(groups)
    return cost(frequencies_counter)
