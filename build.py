import collections
from copy import deepcopy
import random

import config
from solution import Solution

def get_previous_groupmates(person, groups):
    ids_of_previous_groupmates = []
    for group in groups:
        if person in group.people:
            ids_of_previous_groupmates.extend(
                [p.id for p in group.people if p.id != person.id])
    return ids_of_previous_groupmates

def num_groupmates(group, ids_of_previous_groupmates):
    ids_at_group = [person.id for person in group.people]
    intersection = set(ids_at_group) & set(ids_of_previous_groupmates)
    num_prev_groupmates = len(intersection)
    return num_prev_groupmates

def best_group(person, groups, day):
    open_groups = [group for group in groups if group.not_full() and group.day == day]
    if config.greedy:
        ids_of_previous_groupmates = get_previous_groupmates(person, groups)
        open_groups = sorted(open_groups, 
                             key =
                             lambda group : num_groupmates(group, ids_of_previous_groupmates))
        best_group = open_groups[0]
    else:
        best_group = random.choice(open_groups)
    return best_group

def make_groupings(people, groups, day):
    for person in people:
        group = best_group(person, groups, day)
        person.groupings[day] = group.name
        group.people.append(person)
    return groups

def build_guess(people, groups, all_days):
    people_copy = deepcopy(people)
    groups_copy = deepcopy(groups)
    for d in all_days:
        # TODO get subset of people who need a group that day
        random.shuffle(people)
        groups_out = make_groupings(people, groups, d)
    guess = Solution.initial_solution(groups)
    return guess
