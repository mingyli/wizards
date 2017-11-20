
import argparse
import random
import heapq
import numpy as np
import itertools
from itertools import combinations


# for use when keyboard interrupt. 
best_state = (float("inf"), None)

def solve(num_wizards, num_constraints, wizards, constraints):
    global best_state

    def is_conflict(constraint):
        wi, wj, wk = constraint    
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        return (k > i) ^ (k > j)

    num_conflicts = lambda: sum(is_conflict(constraint) for constraint in constraints)

    def swap(i, j):
        wizard_index[wizards[i]], wizard_index[wizards[j]] = wizard_index[wizards[j]], wizard_index[wizards[i]]
        wizards[i], wizards[j] = wizards[j], wizards[i]

    def kick(strength=3):
        for _ in range(strength):
            i, j = random.sample(range(num_wizards), 2)
            swap(i, j)
            

    random.shuffle(wizards)
    wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

    for _ in itertools.count():

        print("=============")
        print("iteration", _)
        print("conflicts", sum(is_conflict(constraint) for constraint in constraints))

        n = 7
        least_conflicts = []

        conflicts = num_conflicts()
        if 0 == conflicts:
            return wizards
        if conflicts < best_state[0]:
            best_state = (conflicts, wizards.copy())

        for i, j in itertools.combinations(range(num_wizards), 2):
            swap(i, j)
            new_conflicts = num_conflicts()

            # terminate early
            if 0 == new_conflicts:
                return wizards

            swap(i, j)

            if len(least_conflicts) == n:
                heapq.heappushpop(least_conflicts, (-new_conflicts, i, j))
            else:
                heapq.heappush(least_conflicts, (-new_conflicts, i, j))


        # if stagnant then kick
        # if all(least_conflicts[0][0] == t[0] for t in least_conflicts):
        if all(-conflicts == t[0] for t in least_conflicts):
            kick(strength=4)
            print("kicked at conflicts", conflicts)
        else:
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
        print("instance halted early.")
        solution = best_state[1]

    write_output(args.output_file, solution)
    print("best state below.")
    print(best_state)
    print("solution:", solution)
