
import os

# first positional argument is 20, 35, or 50. second position argument is the input file number
cmd = "python3 solver.py phase2_inputs/inputs{0}/input{0}_{1}.in outputs/outputs{0}/output{0}_{1}.out > outputs/outputs{0}/output{0}_{1}.log" 
cmd = "python3 solver2_optimized.py {0} {1}"

for file in os.listdir("phase3_inputs"):
    name, ext = file.split('.')
    if name.startswith("sub") and ext == 'in':
        cmd = "python3 solver2_optimized.py phase3_inputs/" + file + " phase3_outputs/" + name + ".out"
        print("executing", cmd)
        os.system(cmd)
        os.system("mv phase3_inputs/" + file + " phase3_inputs/completed" + file[10:])
