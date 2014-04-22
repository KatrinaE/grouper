import random
import copy

import cost_funcs.cf_same_spot as same_spot
import cost_funcs.cf_overlaps as overlaps
import cost_funcs.cf_group_size as group_size
from grouper_io import days_from_groups
import config

class Solution(object):

    def __init__(self, solution, changes = None):
        self.solution = solution

    @classmethod
    def initial_solution(cls, groups):
        solution = cls(groups)
        solution.num_people = len(set([person.id 
                                   for group in groups
                                   for person in group.people]))
        solution.days = days_from_groups(groups)
        solution.create_solution_metrics()
        solution.update_cost()        
        return solution

    @classmethod
    def from_old(cls, old_solution):
        # Copy solution so we don't ruin the old version, which we might need
        # to fall back on.
        old_solution_copy = copy.deepcopy(old_solution)
        new = cls(old_solution_copy.solution)
        new.num_people = old_solution.num_people
        new.days = old_solution.days
        changes = new.choose_changes()
        groups_to_change = changes[0]
        overlaps_before_change = new.overlaps_in_changes(groups_to_change)
        new.make_changes(*changes)
        overlaps_after_change = new.overlaps_in_changes(groups_to_change)
        new.overlaps_changes = [x[0] - x[1] 
                                 for x in zip(overlaps_after_change, overlaps_before_change)]
        new.update_solution_metrics(old_solution_copy)
        return new

    def create_solution_metrics(self):
        # number refers to the group size
        self.overlaps2_matrix = overlaps.create_freqs_matrix(self.solution, self.num_people, 2)
        self.overlaps3_matrix = overlaps.create_freqs_matrix(self.solution, self.num_people, 3)

        self.overlaps2_freqs = overlaps.freqs(self.overlaps2_matrix)
        self.overlaps3_freqs = overlaps.freqs(self.overlaps3_matrix)

        self.same_spot_freqs = same_spot.freqs(self.solution)
        self.update_cost()

    def update_solution_metrics(self, old_solution):
        self.overlaps2_matrix = old_solution.overlaps2_matrix + self.overlaps_changes[2]
        self.overlaps2_freqs = overlaps.freqs(self.overlaps2_matrix)
        self.overlaps3_matrix = old_solution.overlaps3_matrix + self.overlaps_changes[3]
        self.overlaps3_freqs = overlaps.freqs(self.overlaps3_matrix)
        self.same_spot_freqs = same_spot.freqs(self.solution)#old_solution.same_spot_freqs# + **something**
        self.update_cost()

    def update_cost(self):
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

    def overlaps_in_changes(self, groups):
        my_overlaps = [0]*4
        for subgroup_size in (2, 3):
            # only care about pairs and trios, thus '(2, 3)'
            my_overlaps[subgroup_size] = overlaps.create_freqs_matrix(groups, 
                                                                   self.num_people, 
                                                                   subgroup_size)
        return my_overlaps


    def make_changes(self, changes):
        self.make_changes(*self.changes)
        new_overlaps = overlaps.create_freqs_matrix(groups_to_switch, self.num_people, group_size)
        return new_overlaps - old_overlaps

    def choose_changes(self):
        day_to_switch = random.choice(self.days)
        groups_that_day = [t for t in self.solution \
                           if t.day == day_to_switch]
        groups_to_switch = random.sample(groups_that_day, 2)
        person0 = random.choice(groups_to_switch[0].people)
        person1 = random.choice(groups_to_switch[1].people)
        return [groups_to_switch, [person0, person1], day_to_switch]


    def make_changes(self, groups, people, day):
        groups[0].people.remove(people[0])
        groups[0].people.append(people[1])
        groups[1].people.remove(people[1])
        groups[1].people.append(people[0])
        people[0].groupings[day] = groups[1].name
        people[1].groupings[day] = groups[0].name
