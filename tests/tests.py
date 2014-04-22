import unittest
import nose
import os
import math
from collections import Counter

import main
from grouper_io import people_objects, group_objects, Person, days_from_groups, InputData
from solution import Solution
from build import build_guess
from anneal import anneal

class IOTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/tiny-people.csv'
        self.days = ['day0', 'day1', 'day2', 'day3']
    def tearDown(self):
        pass
    
    def test_people_objects(self):
        """
        test going from input file to people objects
        """
        people = people_objects(self.filename, self.days)
        nose.tools.assert_equal(len(people), 4)
        expected_names = set(["Paul Cook", "Stacey Adams", "Rosemary Smith", "Robert Jones"])
        actual_names = set([p.name for p in people])
        nose.tools.assert_equal(expected_names, actual_names)
        expected_ids = set([1,2,3,4])
        actual_ids = set([p.id for p in people])
        nose.tools.assert_equal(expected_ids, actual_ids)

        for p in people:
            for d in self.days:
                nose.tools.assert_equal(getattr(p, d), '')

    def test_group_objects(self):
        """
        Test going from basic information to group objects
        """
        groups = group_objects(self.days, num_groups=3, size_of_groups=3)
        nose.tools.assert_equal(len(groups), 12)
        for d in self.days:
            groups_that_day = [g for g in groups if g.day == d]
            nose.tools.assert_equal(len(groups_that_day), 3)
        for g in groups:
            nose.tools.assert_equal(g.people, [])
            nose.tools.assert_equal(g.capacity, 3)
            nose.tools.assert_true(hasattr(g,'name')) 

        days_out = days_from_groups(groups)
        nose.tools.assert_equal(set(self.days), set(days_out))

class CostFuncTestCase(unittest.TestCase):
    def setUp(self):
        # Create a fixture of people who have already placed in groups
        # for use in testing cost functions.
        # The metrics on this group are:
        # 
        # Number of times grouped together
        # Twice: 2, Once: 2
        #
        # Number of times in same spot
        # Twice: 4, Once: 4
        # 
        # All groups are the appropriate size 
        # (N = 4, # per group = 2)
        days = ['day0', 'day1', 'day2']
        self.p1 = Person("Person 1", 1, days)
        self.p1.day0 = 'group 1'
        self.p1.day1 = 'group 0'
        self.p1.day2 = 'group 0'
        self.p2 = Person("Person 2", 2, days)
        self.p2.day0 = 'group 1'
        self.p2.day1 = 'group 0'
        self.p2.day2 = 'group 1'
        self.p3 = Person("Person 3", 3, days)
        self.p3.day0 = 'group 0'
        self.p3.day1 = 'group 1'
        self.p3.day2 = 'group 1'
        self.p4 = Person("Person 4", 4, days)
        self.p4.day0 = 'group 0'
        self.p4.day1 = 'group 1'
        self.p4.day2 = 'group 0'
        self.people = [self.p1, self.p2, self.p3, self.p4]

        num_groups = 2
        size_of_groups = 2

        self.groups = group_objects(days, num_groups, size_of_groups)
        # manually create a solution object
        for g in self.groups:
            for p in self.people:
                if getattr(p, g.day) == g.name:
                    g.people.append(p)
        self.solution = Solution(self.groups)
        self.solution.update_solution_metrics()
    
    def test_cf_overlaps(self):
        expected_freqs2 = Counter({ 2: 2, 1: 2})
        expected_freqs3 = Counter()
        nose.tools.assert_equal(self.solution.overlaps2_freqs, expected_freqs2)
        nose.tools.assert_equal(self.solution.overlaps3_freqs, expected_freqs3)
    
    def test_cf_same_spot(self):
        expected_same_spot = Counter({ 2:4, 1:4})
        nose.tools.assert_equal(self.solution.same_spot_freqs, expected_same_spot)

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.ppl_file = 'tests/tiny-people.csv'

    def tearDown(self):
        pass

    @classmethod
    def _validate_solution(cls, people, days, num_groups, solution):
        """
        Test that the solution has the correct number of people/groups
        and that no person is in two groups on the same day
        """
        groups_out = solution.solution
        # make sure the overall number of groups is correct
        nose.tools.assert_equal(len(groups_out), len(days)*num_groups)
        # make sure each group has the correct number of people
        max_per_group = math.ceil(len(people)/num_groups)
        min_per_group = math.floor(len(people)/num_groups)
        for group_list in [group.people for group in groups_out]:
            nose.tools.assert_true(len(group_list) <= max_per_group)
            nose.tools.assert_true(len(group_list) >= min_per_group)

        # make sure everyone is placed exactly once each day
        for day in days:
            groups_that_day = [g for g in groups_out if g.day == day]
            # make sure each day has the correct number of groups
            nose.tools.assert_equal(len(groups_that_day), num_groups)
            # list the names of everyone who's seated -somewhere- that day.
            all_people_that_day = [p.name for group in groups_that_day for p in group.people]
            # make sure there's the same number of people as we started with
            nose.tools.assert_equal(len(all_people_that_day), len(people))
            # make sure the people are the same ones we started with
            nose.tools.assert_equal(set(all_people_that_day), set([p.name for p in people]))

    def test_build_guess(self):
        """
        Test that there are the correct number of people at each group each day
        """
        input_data = InputData(self.ppl_file,
                           5,
                           None,
                           2,
                           None)
        solution = build_guess(input_data.people, input_data.groups, input_data.days)
        self._validate_solution(input_data.people, input_data.days, input_data.num_groups, solution)

    def test_anneal(self):
        """
        Test that after annealing the solution has the correct number of people/groups
        """
        # TODO: figure out how to change settings in config.py for testing purposes
        input_data = InputData(self.ppl_file,
                           5,
                           None,
                           2,
                           None)
        init_solution = build_guess(input_data.people, input_data.groups, input_data.days)
        gen = anneal(init_solution)
        for (solution, T) in gen:
            best_solution = solution
        print best_solution.cost
        self._validate_solution(input_data.people, input_data.days, input_data.num_groups, best_solution)
