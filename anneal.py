import math
import warnings
import random
import copy

import config
from display_messages import print_acceptance, print_cost_update
from solution import Solution

def acceptance_probability(old_cost, new_cost, T):
    """ Metropolis-Hastings probability function for deciding 
    whether or not to accept a new solution. Based on code from: 
    http://code.activesolution.com/recipes/
    414200-metropolis-hastings-sampler/
    """
    try:
        warnings.simplefilter("error")
        acceptance_probability = min([1.,math.exp((old_cost-new_cost)/T)])
    except RuntimeWarning:
        # neither new nor old cost is probable --> 0/0 situation, just return 0
        acceptance_probability = 0.0
    except OverflowError:
        acceptance_probability = 1
    return acceptance_probability
        

def anneal_at_temp(best_solution, current_solution, T):
    i = 1
    while i < config.iterations_per_temp:
        new_solution = Solution.from_old(current_solution)
        old_cost = current_solution.cost
        new_cost = new_solution.cost

        ap = acceptance_probability(old_cost, new_cost, T)
        r = random.random()

        if ap > r:
            current_solution = new_solution
            print_acceptance(ap, r, new_cost, "ACCEPT")
            if new_cost < best_solution.cost:
                best_solution = copy.deepcopy(new_solution)
                print_cost_update(best_solution.cost)
        print_acceptance(ap, r, new_cost, "REJECT")

        i = i + 1
    return best_solution, current_solution


def anneal(solution):
    """
    Applies a simulated annealing algorithm to improve the generated
    solution. Similar to vanilla hill climbing, but
    accepts moves to worse solutions, especially early on, to avoid
    getting trapped at a local maxima.

    current_solution, current_solution.cost = current solution & cost
    best_solution, best_solution.cost = best solution & cost found so far
    """
    current_solution = best_solution = solution
    T = config.T
    while T > config.T_min and best_solution.cost > config.max_acceptable_cost:
        yield best_solution, T
        best_solution, current_solution = anneal_at_temp(best_solution, current_solution, T)
        T = T*config.alpha
        print best_solution.cost

    yield best_solution, T
