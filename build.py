import collections
import random

import config
from solution import Solution

def today_only(groups, day):
    groups_out = []
    for group in groups:
        if group.day == day:
            groups_out.append(group)
    return groups_out

def not_full(groups):
    open_groups = []
    for group in groups:
        if len(group.people) < int(group.capacity):
            open_groups.append(group)
    if not open_groups:
        raise Error("More people than groups!")
    else:
        return open_groups

def get_previous_seatmates(person, groups):
    ids_of_previous_seatmates = []
    for group in groups:
        if person in group.people:
            ids_of_previous_seatmates.extend([p.id for p in group.people if p.id != person.id])
    return ids_of_previous_seatmates

def ordered_by_num_seatmates(groups, ids_of_previous_seatmates):
    h = []
    for group in groups:
        ids_at_group = [person.id for person in group.people]
        intersection = set(ids_at_group) & set(ids_of_previous_seatmates)
        num_prev_seatmates = len(intersection)
        h.append((num_prev_seatmates, group))
    h.sort()
    groups_out = [tup[1] for tup in h]
    return groups_out

def ordered_by_same_spot(groups, person):
    persons_groups = collections.Counter([v for (k,v) in person.__dict__.iteritems() if k not in ['name', 'id']])
    l = []
    for group in groups:
        tup = (persons_groups[group.name], group)
        l.append(tup)
    l.sort()
    groups_out = [tup[1] for tup in l]
    return groups_out

def best_group(person, groups, day):
    open_groups = today_only(groups, day)
    open_groups = not_full(open_groups)
    if config.greedy:
        ids_of_previous_seatmates = get_previous_seatmates(person, groups)
        #open_groups = ordered_by_same_spot(open_groups, person)
        open_groups = ordered_by_num_seatmates(open_groups, ids_of_previous_seatmates)
        best_group = open_groups[0]
    else:
        best_group = random.choice(open_groups)
    return best_group

def make_groupings(people, groups, day):
    for person in people:
        group_name = getattr(person, day)
        if group_name is '':
            group = best_group(person, groups, day)
            setattr(person, day, group.name)
            group.people.append(person)
    return groups

def build_guess(people, groups, all_days):
    for d in all_days:
        random.shuffle(people)
        groups_out = make_groupings(people, groups, d)
    guess = Solution(groups)
    return guess
