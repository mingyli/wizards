import argparse
import random
import heapq
import itertools
from itertools import combinations

# for use when keyboard interrupt.
best_state = (float("inf"), None)

def solve(num_wizards, num_constraints, wizards, constraints):
    global best_state

    def is_conflict(constraint):
        wi, wj, wk = constraint
        i, j, k = wizard_index[wi], wizard_index[wj], wizard_index[wk]
        return (k > i and k < j) or (k < i and k > j)

    def swap(i, j):
        """Swaps wizard i with wizard j in the ordering
        and updates conflicts accordingly."""
        nonlocal conflicts

        wizard_index[wizards[i]], wizard_index[wizards[j]] = wizard_index[wizards[j]], wizard_index[wizards[i]]

        wizards[i], wizards[j] = wizards[j], wizards[i]

        # for each constraint that involves wizard i or wizard j
        for constraint in set.union(wiz_to_constraints[wizards[i]], wiz_to_constraints[wizards[j]]):
            if constraint_states[constraint] and not is_conflict(constraint):
                # if constraint was violated but is not anymore
                conflicts -= 1
                constraint_states[constraint] = False # set state to false
            if not constraint_states[constraint] and is_conflict(constraint):
                # if constraint was not violated but now it is
                conflicts += 1
                constraint_states[constraint] = True

    def kick(strength=1):
        conflicts = [constraint for constraint in constraints if is_conflict(constraint)]
        for wa, wb, wc in [random.choice(conflicts)]:
            # in a b c swap either a c or b c
            a, b, c = wizard_index[wa], wizard_index[wb], wizard_index[wc]
            if random.random() < 0.5: swap(a, c)
            else: swap(b, c)
        return


    def successors(num_conflicts):
        """Generator for the successor states.
        Does not actually return successors to save on space.
        Returns a sequence of swaps."""
        swap_cap = 99

        i_s = random.sample(range(num_wizards), min(swap_cap, num_wizards))
        j_s = random.sample(range(num_wizards), min(swap_cap, num_wizards))
        for i, j in itertools.product(i_s, j_s):
            yield ((i, j),)


    wizard_index = {wizard: i for i, wizard in enumerate(wizards)}

    constraint_states = {constraint: is_conflict(constraint) for constraint in constraints}

    wiz_to_constraints = {w: set() for w in wizards}
    # map from wizard name to set of constraints it's involved in
    for constraint in constraints:
        for w in constraint:
            wiz_to_constraints[w].add(constraint)

    conflicts = sum(c for c in constraint_states.values())

    for _ in itertools.count():

        print("=============")
        print("iteration", _)
        print("conflicts", conflicts)

        if 0 == conflicts:
            return wizards
        if conflicts <= best_state[0]:
            best_state = (conflicts, wizards.copy())

        n = 9 if conflicts >= 10 else 29
        least_conflicts = [(float("-inf"), None)] * n

        for swaps in successors(conflicts):
            for i, j in swaps: swap(i, j)

            new_conflicts = conflicts

            # terminate early
            if 0 == conflicts:
                best_state = (0, wizards.copy())
                return wizards

            # undo changes
            for i, j in reversed(swaps): swap(i, j)

            heapq.heappushpop(least_conflicts, (-new_conflicts, swaps))

        if all(-conflicts == t[0] for t in least_conflicts):
            # if stagnant then kick
            kick(strength=1)
            print("kicked at conflicts", conflicts)
        else:
            # commit to swaps
            _, swaps = random.choice(least_conflicts)
            for i, j in swaps: swap(i, j)
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
    random.shuffle(wizards)
    constraints = [tuple(constraint) for constraint in constraints]
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

#return order of the wizards from the order given in filename.out
#state is a list of strings where each string corresponds to the name of the wizard
#the position of the string in the list corresponds to the position of the wizard in the ordering
def read_start_state(filename):
    with open(filename) as f:
        state = f.readline().split() #separates by whitespace
    return state


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    parser.add_argument("-s", "--start_state_file", type=str, help = "___.out") #optional
    #need to type -s before argument in command line
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)

    if (args.start_state_file != None):
        wizards = read_start_state(args.start_state_file)

    try:
        solution = solve(num_wizards, num_constraints, wizards, constraints)
    except KeyboardInterrupt:
        print("instance halted early.")
        solution = best_state[1]

    write_output(args.output_file, solution)
    print("best state below.")
    print(best_state)
    print("solution:", solution)