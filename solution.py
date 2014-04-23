import random
import copy

import cost_funcs.cf_same_spot as same_spot
import cost_funcs.cf_overlaps as overlaps
import cost_funcs.cf_group_size as group_size
from grouper_io import days_from_groups
import config

class Solution(object):
    def __init__(self, solution):
        self.solution = solution
        self.days = days_from_groups(self.solution)
        self.update_solution_metrics()
        
    def update_solution_metrics(self):
        # FREQUENCIES
        # number refers to the group size
        self.overlaps2_freqs = overlaps.freqs(self.solution, 2)
        self.overlaps3_freqs = overlaps.freqs(self.solution, 3)
        self.same_spot_freqs = same_spot.freqs(self.solution)
        # COSTS
        self.cost_of_overlaps = overlaps.cost(self.overlaps2_freqs, 2) + \
                                overlaps.cost(self.overlaps3_freqs, 3)
        self.cost_of_same_spot = same_spot.cost(self.same_spot_freqs)
        self.cost_of_group_size = group_size.cost(self.solution)
        self.cost = self._calc_cost()

    def _calc_cost(self):
        cost = self.cost_of_same_spot + \
               self.cost_of_overlaps + \
               self.cost_of_group_size
        return cost

    def move_to_neighbor(self):
        day_to_switch = random.choice(self.days)
        groups_that_day = [t for t in self.solution \
                           if t.day == day_to_switch]
        groups_to_switch = random.sample(groups_that_day, 2)
        person0 = random.choice(groups_to_switch[0].people)
        person1 = random.choice(groups_to_switch[1].people)

        # performance optimization - pass switchback_args along in case the new solution is not
        # accepted and we need to revert 'groups' to its old state. The alternative
        # is to make a deep copy of 'groups' so that old_solution.groups and
        # new_solution.groups point at completely different things, but this was 
        # causing unacceptable performance degradation.
        self.switch_args = [groups_to_switch[0], person0, groups_to_switch[1], person1]
        self.switchback_args = [groups_to_switch[1], person0, groups_to_switch[0], person1]
        self._group_switch(*self.switch_args)
        self.update_solution_metrics()

    def move_back_from_neighbor(self):
        self._group_switch(*self.switchback_args)
        self.update_solution_metrics()

    def _group_switch(self, group0, person0, group1, person1):
        group0.people.remove(person0)
        group0.people.append(person1)
        group1.people.remove(person1)
        group1.people.append(person0)
        setattr(person0, group0.day, group1.name)
        setattr(person1, group0.day, group0.name)
