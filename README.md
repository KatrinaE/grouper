reGrouper is a Python desktop application for putting people
in 'optimal' groups - ones in which as few people as possible
are in the same group more than once or are paired with the
same person multiple times. It is useful for tasks
like assigning students to groups that rotate each month
or generating seating charts for a multi-day event.

reGrouper can be run either from the command line
or from a GUI.


###Installation
The reGrouper GUI requires matplotlib and numpy,
both of which can be installed with pip:

    pip install numpy
    pip install matplotlib

To run the tests, you'll need nose:

    pip install nose

Install reGrouper by cloning this repository:

    git clone https://github.com/KatrinaE/grouper.git </your/desired/path/to/grouper>

(Note: reGrouper was written for Python 2.7.6. It has not been tested with
other versions.)

###Running from the Command Line
To run reGrouper from the command line, use

    grouper <people file> <num days> -s <size of groups>

or

    grouper <people file> <num days> -n <number of groups>

`people file` is a .csv or .txt file containing peoples' names, one per line.
`num days` is the number of days, or rounds, you are making groups for.
`size of groups` is the preferred size of each group.
`number of groups` is the preferred number of groups.

reGrouper requires that you enter either `size of groups` or 
`number of groups`, but not both.


If you'd like to run reGrouper from anywhere, mark reGrouper's main.py
as executible and add it to your path:

    cd path-to-grouper
    chmod u+x main.py
    ln -s path-to-grouper/main.py /usr/local/bin/grouper

Now you can run, e.g.:

    grouper <people file> <num days> -n <number of groups>

from any directory.

reGrouper's output is a CSV file containing the 
lists of individuals sitting at each table on each day.
By default, it is named 'output.csv'. You can change its name
by using the `-f` option in the command line, e.g:

    grouper <people file> <num days> -n <number of groups> -f <filename>

###Running from the GUI
reGrouper comes with a simple GUI*. To start the GUI from the command line, run:

    python grouper-gui.py

###Optimization Rules
reGrouper uses the following criteria:
* Produce groups of the requested size and number
* Minimize the number of pairs grouped together multiple times.
* Minimize the number of trios grouped together multiple times.
* Minimize the number of people placed in the same spot (e.g. Group 5)
  multiple times.

###Algorithm
reGrouper utilizes two separate algorithms: a simple greedy
strategy that populates the tables day-by-day, placing 
each person at the spot that seems most optimal for
him when his name is drawn, and a simulated annealing
algorithm that generates a solution and switches people
around repeatedly in a search for the optimal solution.
(For the curious, I've written a [blog post about simulated
annealing](http://katrinaeg.com/simulated-annealing.html).

By modifying the `greedy` and `anneal` settings in
`config.py`, you can turn these two parts of the algorithm
on and off independently. I've found I get the best solutions
when both of them are enabled:

    greedy = True # turns on greedy algorithm
    anneal = True # turns on simulated annealing

If `anneal` is True but `greedy` is False, the annealing algorithm
begins from a random solution. If both are set to False, reGrouper
returns a random solution.

###Preferences
reGrouper comes with the following configuration settings, set in
`config.py`:

| Config Parameter | Possible Values | Purpose |
|------------------|-----------------|---------|
| `greedy`         | (True/False)    | Enable/disable the greedy grouping algorithm |
| `anneal`| (True/False) | Enable/disable the annealing algorithm |
| `display_progress` | (True/False) | If True, displays the current temperature and best cost at the end of each annealing iteration.|
| `verbose` | (True/False) | Print debugging messages |
| `super_verbose` | (True/False) | Print even more debugging messages |
| `num_tries` | (integer >= 1) | The number of attempts to make. Default is 1.|
|     |              |                                                  |
| `T` | (float >= 0) | the initial annealing temperature. Default is 1. |
| `alpha` | (float between 0 and 1) | The proportion by which to decrease `T` at the end of each annealing iteration. Default is 0.95. |
| `T_min` | (float between 0 and `T`) | The temperature at which to stop if an acceptable solution has not yet been found. Default is 0.001. |
| `max_acceptable_cost` | (int >= 0) | The cost at which to stop searching for a better solution and return the current one. Default is 0, which corresponds with perfectly satisfying all constraints. |
| `iterations_per_temp` | (int >= 0) | the number of switches to make at each temperature while annealing. Default is 500. |

The last five parameters correspond with simulated annealing.

###Performance
reGrouper's performance is hampered by the expense of computing its cost functions.
Depending on the specific parameters, generating groupings of 100 people can take
15-30 minutes. If you just need a 'good-enough' grouping, set the `anneal` setting
to False.

\* Like the rest of reGrouper, 
the GUI is written in Python, using the Tkinter library. reGrouper has a desktop
interface rather than a web one because it is descended from an earlier
desktop application.