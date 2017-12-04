
import os


for file in os.listdir("phase3_inputs"):
    name, ext = file.split('.')
    print(name, name[9:])
    cmd = "python3 output_validator.py phase3_inputs/" + file + " phase3_outputs/submission" + name[9:] + ".out"
    print(cmd)
    os.system(cmd)
    """
    if name.startswith("sub") and ext == 'in':
        cmd = "python3 solver2_optimized.py phase3_inputs/" + file + " phase3_outputs/" + name + ".out"
        print("executing", cmd)
        os.system(cmd)
        os.system("mv phase3_inputs/" + file + " phase3_inputs/completed" + file[10:])
    """
