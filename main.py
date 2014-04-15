from copy import deepcopy
import math
import argparse

import config
from grouper_io import people_objects, group_objects, write_to_csv, days_from_groups
from build import build_guess
from anneal import anneal
from display_messages import display_settings, display_init_cost, \
    display_result, display_annealing_progress
from solution import Solution

def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def create_parser():
    parser = argparse.ArgumentParser(description="Run the Grouper command-line app")
    parser.add_argument("people_file", action="store")
    parser.add_argument("num_days", type=check_negative, action="store")
    parser.add_argument("-f", "--output_filename", action="store")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--size-of-groups", type=check_negative, action='store')
    group.add_argument("-n", '--num-groups', type=check_negative, action="store")
    return parser

def get_data(people_csv, num_days, num_groups, size_of_groups):
    days = [('day' + str(i)) for i in range(0, int(num_days))]
    people = people_objects(people_csv, days)
    if size_of_groups != '' and size_of_groups != None:
        size_of_groups = int(size_of_groups)
        num_groups = int(math.ceil(len(people)/float(size_of_groups)))
    elif num_groups != '' and num_groups != None:
        num_groups = int(num_groups)
        size_of_groups = int(math.ceil(len(people)/float(num_groups)))
    else:
        raise RuntimeError("Either the group size or the number of groups must be set")

    groups = group_objects(days, num_groups, size_of_groups)

    return people, groups, days, num_groups, size_of_groups

def main_gui(people_csv, num_days, num_groups, size_of_groups):
    """
    This is the main entry point for the Python GUI.
    We have to do this completely separately from 'main' because
    including the 'yield' statement makes this function a generator,
    which prevents it from working on the command line.
    """
    
    people, groups, days, num_groups, size_of_groups = get_data(
        people_csv, num_days, num_groups, size_of_groups)

    people_copy = deepcopy(people)
    groups_copy = deepcopy(groups)
    init_solution = build_guess(people_copy, groups_copy, days)
    
    best_solution = init_solution
    for i in range(0, config.num_tries):
        people_copy = deepcopy(people)
        groups_copy = deepcopy(groups)
        init_solution = build_guess(people_copy, groups_copy, days)

        if config.verbose:
            display_init_cost(init_solution.cost)

        if config.anneal:
            gen = anneal(init_solution)
            for (best_solution, T) in gen:
                if config.display_progress:
                    display_annealing_progress(best_solution.cost, T)
                yield best_solution, T
        else:
                best_solution = init_solution


def main(people_csv, num_days, num_groups, size_of_groups, output_filename='output.csv'):
    if config.verbose:
        print "*************************************"
        display_settings()
    
    people, groups, days, num_groups, size_of_groups = get_data(
        people_csv, num_days, num_groups, size_of_groups)

    people_copy = deepcopy(people)
    groups_copy = deepcopy(groups)
    init_solution = build_guess(people_copy, groups_copy, days)
    
    best_solution = all_time_greatest = init_solution
    for i in range(0, config.num_tries):
        people_copy = deepcopy(people)
        groups_copy = deepcopy(groups)
        init_solution = build_guess(people_copy, groups_copy, days)

        if config.verbose:
            display_init_cost(init_solution.cost)

        if config.anneal:
            gen = anneal(init_solution)
            for (best_solution, T) in gen:
                if config.display_progress:
                    display_annealing_progress(best_solution.cost, T)

        else:
                best_solution = init_solution

        if best_solution.cost < all_time_greatest.cost:
            all_time_greatest = best_solution

    print "FINAL SOLUTION"
    print "The best cost found is: " + str(all_time_greatest.cost)
    print "Pairs overlapping: " + str(all_time_greatest.overlaps2_freqs)
    print "Trios overlapping: " + str(all_time_greatest.overlaps3_freqs)
    print "Same spots: " + str(all_time_greatest.same_spot_freqs)
    print "Table size: " + str(all_time_greatest.cost_of_group_size)

    # Write to file
    write_to_csv(all_time_greatest.solution, days, filename)

    if config.verbose:
        display_result(best_solution.cost)
        print "************************************"

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args.people_file, args.num_days, args.num_groups, args.size_of_groups, output_filename=args.output_filename)
