import json

with open('failure-Andrew-50-0.txt') as datafile:
    data = json.load(datafile)
f = open("output_andrew50-0.txt", 'w')
f.write("50")
f.write('\n')
f.write(" ".join(str(i) for i in data[0]))
f.write('\n')
f.write("360")
f.write('\n')
for constraint in data[1]:
    f.write(" ".join(str(i) for i in constraint))
    f.write('\n')
f.close()
