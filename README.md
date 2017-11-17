
1. given a constraint `a b c`, we can construct the boolean expression

(c > a & c > b) | (c < a & c < b)


### potential tricks
- sort wizards alphanumerically and check, if other competitors aren't careful with inputs
- both the sequence and the reverse satisfy the constraints


## to run
`python3 solver.py inputs/input15.in samples/input15.out`
`python3 output_validator.py inputs/input15.in samples/input15.out`
