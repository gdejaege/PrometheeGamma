#import numpy as np

#rval0__1 = np.arange(0.01, 1.01, 0.01)
#rval0_1 = [i for i in range(0, 101)]


#print(rval0__1)

p1 = (0,3)

p2 = (5,6)

p = []
p.append(p1)
p.append(p2)
p = tuple(p)
p3 = (0,3), (5,6)


print(p)
print(p3)