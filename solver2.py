
import argparse
import random
import heapq
import numpy as np
import itertools
from itertools import combinations



def solve(num_wizards, num_constraints, wizards, constraints):

    # mapping from wizard name to index
    wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

    def is_conflict(constraint):
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        return (k > i) ^ (k > j)

    num_conflicts = lambda: sum(is_conflict(constraint) for constraint in constraints)

    def swap(i, j):
        wizards[i], wizards[j] = wizards[j], wizards[i]

    for _ in itertools.count():
        print("=============")
        print("iteration", _)
        print("conflicts", sum(is_conflict(constraint) for constraint in constraints))

        n = 9
        least_conflicts = []

        conflicts = num_conflicts()
        if 0 == conflicts:
            return wizards

        for i, j in itertools.combinations(range(num_wizards), 2):
            swap(i, j)
            wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

            conflicts = num_conflicts()

            # terminate early
            if 0 == conflicts:
                return wizards

            if len(least_conflicts) == n:
                heapq.heappushpop(least_conflicts, (-conflicts, i, j))
            else:
                heapq.heappush(least_conflicts, (-conflicts, i, j))

            swap(i, j)

        _, i, j = random.choice(least_conflicts)
        swap(i, j)
    return wizards


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

    print("solution:", solution)
    write_output(args.output_file, solution)
