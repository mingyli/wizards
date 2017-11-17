import json

with open('failure-Andrew-35-0.txt') as datafile:
    data = json.load(datafile)
f = open("output_andrew35-0.txt", 'w')
f.write("35")
f.write('\n')
f.write(" ".join(str(i) for i in data[0]))
f.write('\n')
f.write("280")
f.write('\n')
for constraint in data[1]:
    f.write(" ".join(str(i) for i in constraint))
    f.write('\n')
f.close()
