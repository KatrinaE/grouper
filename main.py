from copy import deepcopy
import math
import argparse

import config
from grouper_io import InputData, write_to_csv
from build import build_guess
from anneal import anneal
from display_messages import print_settings, print_init_cost, print_progress, print_final_metrics
from solution import Solution

def check_negative(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("'%s' is not a positive integer" % value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is not a positive integer" % value)
    return ivalue

def create_parser():
    parser = argparse.ArgumentParser(description="Run the Grouper command-line app")
    parser.add_argument("people_file", action="store")
    parser.add_argument("num_days", type=check_negative, action="store")
    parser.add_argument("-f", "--output_filename", default='output.csv', action="store")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--size-of-groups", type=check_negative, action='store')
    group.add_argument("-n", '--num-groups', type=check_negative, action="store")
    return parser


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
            print_init_cost(init_solution.cost)

        if config.anneal:
            gen = anneal(init_solution)
            for (best_solution, T) in gen:
                if config.print_progress:
                    print_annealing_progress(best_solution.cost, T)
                yield best_solution, T
        else:
                best_solution = init_solution

def main(input_data):
    print "*************************************"
    print_settings()
    
    best_solution = None
    for i in range(0, config.num_tries):
        solution = build_guess(input_data.people, input_data.groups, input_data.days)

        print_init_cost(solution.cost)

        if config.anneal:
            for (solution, T) in anneal(solution):
                print_progress(solution, T)

            if best_solution == None or solution.cost < best_solution.cost:
                best_solution = solution

    print_final_metrics(best_solution)
    write_to_csv(best_solution.solution, best_solution.days, output_filename)
    print "************************************"

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    input_data = InputData(args.people_file, 
                           args.num_days, 
                           args.num_groups, 
                           args.size_of_groups, 
                           args.output_filename)
    main(input_data)
