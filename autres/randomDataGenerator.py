import random as rnd

output = "./Data/randomDataSet.csv"
nbCriteria = 20
nbAlternatives = 100

file = open(output, "w")

line = "c"
for i in range(nbCriteria):
    line += ",g" + str(i)
file.write(line+"\n")

for j in range(nbAlternatives):
    line = "a" + str(j)
    for k in range(nbCriteria):
        line += "," + str(rnd.randint(0,100))
    file.write(line+"\n")

line = "w"
for l in range(nbCriteria):
    line += "," + str(1.0/nbCriteria)
file.write(line+"\n")

line = "f"
for m in range(nbCriteria):
    line += "," + str(rnd.randint(1,6))
file.write(line+"\n")

line = "p"
for n in range(nbCriteria):
    line += "," + str(rnd.randint(10,20))
file.write(line+"\n")

line = "q"
for o in range(nbCriteria):
    line += "," + str(rnd.randint(1,5))
file.write(line+"\n")

file.close()




