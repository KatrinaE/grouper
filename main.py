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

def main(input_data):
    best_solution = None
    for i in range(0, config.num_tries):
        solution = build_guess(input_data.people, input_data.groups, input_data.days)

        print_init_cost(solution.cost)

        if config.anneal:
            for (solution, T) in anneal(solution):
                print_progress(solution, T)
                if best_solution == None or solution.cost < best_solution.cost:
                    best_solution = deepcopy(solution)
                yield best_solution, T

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    input_data = InputData(args.people_file, 
                           args.num_days, 
                           args.num_groups, 
                           args.size_of_groups, 
                           args.output_filename)

    for (solution, T) in main(input_data):
        print_progress(solution, T)

    print_final_metrics(solution)
    write_to_csv(solution.solution, input_data.days, input_data.output_filename)
