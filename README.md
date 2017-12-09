You are at another wizard party hosted by Prasad and Sanjam. As usual, wizards are shy about discussing
their age. From conversations at the party, you are only given information in the following form: some
wizard’s age is not between the ages of two other wizards. Since wizard parties are also notoriously long
(an entire month!), you decide to use your time at the party to write a solver and figure out the true ordering
of wizards by their ages.


1. given a constraint `a b c`, we can construct the boolean expression

(c > a & c > b) | (c < a & c < b)


### potential tricks
- sort wizards alphanumerically and check, if other competitors aren't careful with inputs
- both the sequence and the reverse satisfy the constraints


## to run
`python3 solver.py inputs/input15.in samples/input15.out`
`python3 output_validator.py inputs/input15.in samples/input15.out`
