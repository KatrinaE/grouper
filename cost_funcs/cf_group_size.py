def cost(groups, verbose=False):
    """Distance of each group from its capacity"""
    maximum = 0
    cost = 0
    for group in groups:
        distance_from_capacity = len(group.people) - int(group.capacity)
        cost += abs(distance_from_capacity)**4
        maximum = max(maximum, abs(distance_from_capacity))
        if verbose == True:
            print str(group.name) + " on " + str(group.day) + " is " + str(distance_from_capacity) + " away from optimal capacity "
    return cost
