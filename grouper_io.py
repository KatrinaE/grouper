import csv
import math
import collections

class InputData(object):
    def __init__(self, people_file, num_days, num_groups, size_of_groups, output_filename):
        self.days = self._make_days(num_days)
        self.people = people_objects(people_file, self.days)
        self.num_people = len(self.people)
        self.num_groups, \
            self.size_of_groups = self._group_constraints(self.num_people,
                                                    num_groups, 
                                                    size_of_groups)
        self.groups = group_objects(self.days, self.num_groups, self.size_of_groups)
        if output_filename != None:
            self.output_filename = output_filename
        else:
            self.output_filename = "output.csv"

    def _make_days(self, num_days):
        return [('day' + str(i)) for i in range(0, int(num_days))]

    def _quotient(self, dividend, divisor):
        float_divisor = float(divisor)
        float_quotient = math.ceil(dividend/float_divisor)
        int_quotient = int(float_quotient)
        return int_quotient

    def _group_constraints(self, num_people, num_groups, size_of_groups):
        if size_of_groups != None:
            size_of_groups = int(size_of_groups)
            num_groups = self._quotient(num_people, size_of_groups)
        elif num_groups != None:
            num_groups = int(num_groups)
            size_of_groups = self._quotient(num_people, num_groups)
        return num_groups, size_of_groups


class Person(object):
    def __init__(self, id, name, days):
        self.id = id
        self.name = name
        for day in days:
            setattr(self, day, '')

def people_objects(filename, days):
    current_id = 1
    people_list = []
    with open(filename, 'r') as f:
        for line in f:
            name = line
            person = Person(current_id, name, days)
            people_list.append(person)
            current_id += 1
    return people_list

class Group(object):
    def __init__(self, name, day, capacity):
        self.name = name
        self.day = day
        self.capacity = capacity
        self.people = []

def group_objects(days, num_groups, size_of_groups):
    '''
    Creates a list of objects, 1 for each group
    '''
    groups = []
    for i in range(0, num_groups):
        name = "group " + str(i)
        for day in days:
            capacity = size_of_groups
            group_object = Group(name, day, capacity)
            groups.append(group_object)
    return groups

def days_from_groups(groups):
    days = list(set(g.day for g in groups))
    return days

def write_to_csv(groups, days, filename):
    all_groups = {}
    for group in groups:
        all_groups[group.name] = { 'Name' : group.name}
        for day in days:
            all_groups[group.name][day] = None
    for group in groups:
            people_list = [p.name for p in group.people]
            all_groups[group.name][group.day] = ', '.join([p for p in people_list])
    all_out = []
    for (k, v) in all_groups.iteritems():
            all_out.append(v)

    fieldnames = ['Name']
    fieldnames.extend(days)
    with open(filename,'w') as file:
        csvwriter = csv.DictWriter(file, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
        csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
        for group in all_out:
            csvwriter.writerow(group)
