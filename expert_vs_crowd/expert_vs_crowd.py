import numpy as np
import matplotlib.pyplot as plt
import operator as op
from functools import reduce
from scipy.stats import norm
import math

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

#note that this is an approximation
def expert_chooses(n, mean, std):
    x = (n - (math.pi / 8))/(n - (math.pi / 4) + 1)
    return min(1, mean + std * norm.ppf(x))

def crowd_chooses(n, mean, std):
    total = 0
    for i in range(int((n+1)/2), n+1):
        total += ncr(n,i) * np.power(mean, i) * np.power((1-mean), n-i)
    return total


mean = float(input("Please give mean accuracy of the crowd"))
std = float(input("Please give the standard deviation of the accuracy"))
y1 = []
y2 = []
for i in range(3,100,2):
    print(i)
    expert_acc = expert_chooses(i, mean, std)
    crowd_acc = crowd_chooses(i, mean, std)
    print("Expert accuracy: ", expert_acc)
    y1.append(expert_acc)
    print("Crowd accuracy: ", expert_acc)
    y2.append(crowd_acc)

fig, ax = plt.subplots(1, 1, figsize=(6, 4))
x = [i for i in range(3,100,2)]
ax.plot(x, y1, '-', label="Expert Accuracy")
ax.plot(x, y2, '-', label="Crowd Accuracy")
ax.legend()
plt.show()
