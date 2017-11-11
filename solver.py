import argparse
import random
import numpy as np
from itertools import combinations

"""
======================================================================
  Complete the following function.
======================================================================
"""

# for use when keyboard interrupt. (conflicts, state graph)
best_state = (float("inf"), None)

def ordered(state):
    """Returns wizards in sorted order given the state graph.
    
    >>> wizards = ['A', 'B', 'C']
    >>> num_wizards = len(wizards)
    >>> state = np.matrix([[None, 1, 1], [0, None, 1], [0, 0, None]])
    >>> ordered(state)
    ['A', 'B', 'C']

    To topologically sort, need to take wizard that is greater than 
    the highest number of wizards.
    """
    def topological_sort(w):
        """Use reverse postorder."""
        visited[w] = True
        neighbors = [n for n in range(num_wizards) if state[w, n]]
        for neighbor in neighbors:
            if not visited[neighbor]:
                topological_sort(neighbor)
        stack.insert(0, w)

    visited = [False for _ in range(num_wizards)]
    stack = []
    for i in range(num_wizards):
        if not visited[i]:
            topological_sort(i)
    return [wizards[i] for i in stack]

def kick(state):
    for _ in range(num_wizards // 7):
        i, j = random.randrange(num_wizards), random.randrange(num_wizards)
        if state[i, j] is not None:
            state[i, j] = not state[i, j]
            state[j, i] = not state[j, i]

        
def solve(num_wizards, num_constraints, wizards, constraints, MAX_ITER=9999):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']

    Output:
        An array of wizard names in the ordering your algorithm returns


    >>> wizards = ['w1', 'w2', 'w0']
    >>> constraints = [('w0', 'w1', 'w2'), ('w1', 'w2', 'w0')]
    >>> order = solve(len(wizards), len(constraints), wizards, constraints)
    >>> order == ['w1', 'w2', 'w0'] or order == ['w0', 'w2', 'w1']
    True
    """

    # for use when keyboard interrupt
    global best_state

    def is_conflict(constraint):
        """Returns whether the state does not satisfy the constraint."""
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        if state[k, i] is None or state[k, j] is None:
            return True
        return bool(state[k, i]) ^ bool(state[k, j])

    def toggle(i, j):
        state[i, j], state[j, i] = not state[i, j], not state[j, i]

    # mapping from wizard name to index
    wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

    # a state graph such that state[i, j] returns whether wizard i > wizard j
    # the value is None if we have not set the condition yet
    # conveniently, `not None` evaluates to True, which helps below
    state = np.matrix(np.full((num_wizards, num_wizards), None))
    for constraint in constraints:
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        state[i, k], state[k, i] = True, False
        state[j, k], state[k, j] = True, False

    prev_conflicts = None
    for _ in range(MAX_ITER):
        print("=============")
        print("iteration", _)

        conflicts = sum(is_conflict(c) for c in constraints)
        print("conflicts", conflicts)

        if conflicts < best_state[0]:
            best_state = (conflicts, state)

        # terminal solution
        if 0 == conflicts:
            return ordered(state)

        # local optimum
        elif conflicts == prev_conflicts:
            kick(state)

        else:
            # change state by greedily selecting least conflicts in neighborhood
            # TODO consider expanding neighborhood to two changes,
            #      randomly select among least conflicts in neighborhood

            # search for position of least conflicts change
            least_conflicts = conflicts
            least_row, least_col = -1, -1
            for i in range(num_wizards):
                for j in range(i):
                    # set state[i, j] to argmax conflicts
                    # state[i, j], state[j, i] = not state[i, j], not state[j, i]
                    toggle(i, j)
                    new_conflicts = sum(is_conflict(c) for c in constraints)
                    if new_conflicts <= least_conflicts:
                        least_conflicts = new_conflicts
                        least_row, least_col = i, j
                    # state[i, j], state[j, i] = not state[i, j], not state[j, i]
                    toggle(i, j)

            # update by least conflicts 
            # print("least conflicts", least_row, least_col)
            # state[least_row, least_col] = not state[least_row, least_col] 
            # state[least_col, least_row] = not state[least_col, least_row] 
            toggle(least_row, least_col)

        prev_conflicts = conflicts

    # give up after MAX_ITER iterations
    return ordered(state)

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        wizards = f.readline().split()
        num_constraints = int(f.readline())
        constraints = []
        # wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            # for w in c:
            #     wizards.add(w)
                
    wizards = list(set(wizards))
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)

    try:
        solution = solve(num_wizards, num_constraints, wizards, constraints)
    except KeyboardInterrupt:
        print("instance halted early. best result below.")
        print(best_state)
        solution = ordered(best_state[1])

    write_output(args.output_file, solution)
