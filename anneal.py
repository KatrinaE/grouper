import math
import warnings
import random
import copy

import config
from display_messages import display_acceptance, display_cost_update
from solution import Solution

def acceptance_probability(old_cost, new_cost, T):
    """ Metropolis-Hastings probability function for deciding 
    whether or not to accept a new solution. Based on code from: 
    http://code.activestate.com/recipes/
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
        

def anneal_at_temp(best_state, current_state, T):
    i = 1
    while i < config.iterations_per_temp:
        old_cost = current_state.cost
        current_state.move_to_neighbor()
        new_cost = current_state.cost


        ap = acceptance_probability(old_cost, new_cost, T)
        r = random.random()

        if ap > r:
            if config.super_verbose:
                display_acceptance(ap, r, new_cost, "ACCEPT")
            if new_cost < best_state.cost:
                best_state = copy.deepcopy(current_state)
                if config.super_verbose:
                    display_cost_update(best_state.cost)
                
        else:
            current_state.move_back_from_neighbor()


            if config.super_verbose:
                display_acceptance(ap, r, new_cost, "REJECT")

        i = i + 1
    return best_state, current_state


def anneal(solution):
    """
    Applies a simulated annealing algorithm to improve the generated
    seating chart solution. Similar to vanilla hill climbing, but
    accepts moves to worse states, especially early on, to avoid
    getting trapped at a local maxima.

    current_state, current_state.cost = current state & cost
    best_state, best_state.cost = best state & cost found so far
    """
    current_state = best_state = solution
    T = config.T
    while T > config.T_min and best_state.cost > config.max_acceptable_cost:
        yield best_state, T
        best_state, current_state = anneal_at_temp(best_state, current_state, T)
        T = T*config.alpha

    yield best_state, T
