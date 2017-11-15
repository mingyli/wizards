import argparse
import random
import heapq
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

    """
    def topological_sort(w):
        """Use reverse postorder."""
        visited[w] = True
        neighbors = [n for n in range(num_wizards) if state[n, w]]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not visited[neighbor]:
                topological_sort(neighbor)
        stack.append(w)

    visited = [False for _ in range(num_wizards)]
    stack = []
    vertices = list(range(num_wizards))
    random.shuffle(vertices)
    for i in vertices:
        if not visited[i]:
            topological_sort(i)
    return [wizards[i] for i in stack]

        
def solve(num_wizards, num_constraints, wizards, constraints, MAX_ITER=99999):
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

    def toggle(i, j):
        state[i, j], state[j, i] = not state[i, j], not state[j, i]

    def fix_cycles(state):
        """Detect cycle and flip edge to fix cycle."""
        def dfs(w):
            visited[w] = True
            ancestors.add(w)
            neighbors = [n for n in range(num_wizards) if state[n, w]]
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if neighbor in ancestors: # flip edge
                    toggle(neighbor, w)
                    return
                if not visited[neighbor]:
                    dfs(neighbor)
            ancestors.remove(w)

        visited = [False for _ in range(num_wizards)]
        ancestors = set()
        vertices = list(range(num_wizards))
        random.shuffle(vertices)
        for i in vertices:
            if not visited[i]:
                dfs(i)

    def is_conflict(constraint):
        """Returns whether the state does not satisfy the constraint."""
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        if state[k, i] is None or state[k, j] is None:
            return True
        return bool(state[k, i]) ^ bool(state[k, j])

    def satisfy(constraint, left=True):
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        state[i, k], state[k, i] = left, not left
        state[j, k], state[k, j] = left, not left

    def kick(state, strength=0.1):
        for _ in range(int(num_constraints * strength)):
            """
            i, j = random.randrange(num_wizards), random.randrange(num_wizards)
            if state[i, j] is not None:
                toggle(i, j)
            """
            constraint = random.choice(constraints)
            wi, wj, wk = constraint
            i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
            satisfy(constraint, left=random.random() < 0.5)

    # mapping from wizard name to index
    wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

    # a state graph such that state[i, j] returns whether wizard i > wizard j
    # the value is None if we have not set the condition yet
    # conveniently, `not None` evaluates to True, which helps below
    state = np.matrix(np.full((num_wizards, num_wizards), None))
    for constraint in constraints:
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        state[i, k], state[k, i] = False, True
        state[j, k], state[k, j] = False, True

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
            print("attempting to fix cycle")
            fix_cycles(state)
            conflicts = sum(is_conflict(c) for c in constraints)
            print("conflicts after fixing cycle is", conflicts)
            if 0 == conflicts:
                return ordered(state)

        # local optimum
        elif conflicts == prev_conflicts:
            kick(state, strength=0.05)
            print("kicked at", conflicts, "conflicts")

        else:
            # change state by greedily selecting least conflicts in neighborhood
            # TODO consider expanding neighborhood to two changes,
            #      randomly select among least conflicts in neighborhood

            # use a heap to get the n best conflict changes
            # need to use a max heap to get the n changes with least conflicts
            n = 3
            best_conflicts = []
            """
            Strategy: change a particular edge
            for i in range(num_wizards):
                for j in range(i):
                    toggle(i, j)
                    new_conflicts = sum(is_conflict(c) for c in constraints)
                    if len(best_conflicts) == n:
                        heapq.heappushpop(best_conflicts, (-new_conflicts, i, j))
                    else:
                        heapq.heappush(best_conflicts, (-new_conflicts, i, j))
                    toggle(i, j)

            # update by least conflicts 
            _, i, j = random.choice(best_conflicts)
            toggle(i, j)
            """

            # Strategy: satisfy a particular constraint, either left or right
            for constraint in constraints:
                wi, wj, wk = constraint    
                i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]

                # store for reset at end of iteration
                store = state[i, k], state[k, i], state[j, k], state[k, j]

                # compare whether satisfying left or right is better
                satisfy(constraint, left=True)
                left_conflicts = sum(is_conflict(c) for c in constraints)
                satisfy(constraint, left=False)
                right_conflicts = sum(is_conflict(c) for c in constraints)
                if left_conflicts > right_conflicts:
                    new_conflicts, left = right_conflicts, False
                else:
                    new_conflicts, left = left_conflicts, True

                # update heap with best n values
                if len(best_conflicts) == n:
                    heapq.heappushpop(best_conflicts, (-new_conflicts, constraint, left))
                else:
                    heapq.heappush(best_conflicts, (-new_conflicts, constraint, left))

                state[i, k], state[k, i], state[j, k], state[k, j] = store
            
            _, constraint, left = random.choice(best_conflicts)
            satisfy(constraint, left)

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
        # wizards = f.readline().split()
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
                
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
        print("instance halted early. best state below.")
        print(best_state)
        solution = ordered(best_state[1])

    write_output(args.output_file, solution)
    print("best state below.")
    print(best_state)
    print(solution)
