
import subprocess
import os

# first positional argument is 20, 35, or 50. second position argument is the input file number
cmd = "python3 solver.py phase2_inputs/inputs{0}/input{0}_{1}.in outputs/outputs{0}/output{0}_{1}.out > outputs/outputs{0}/output{0}_{1}.log" 

for i in range(6, 10):
	subprocess.run(cmd.format(20, 5), shell=True)
