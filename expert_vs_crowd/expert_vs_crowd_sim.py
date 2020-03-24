import numpy as np
import matplotlib.pyplot as plt

def expert_chooses(crowd):
    expert = max(crowd)
    if np.random.uniform(0,1) < expert:
        return 1
    else:
        return 0

def crowd_chooses(crowd):
    ballots = []
    for c in crowd:
        if np.random.uniform(0,1) < c:
            ballots.append(1)
        else:
            ballots.append(0)
    if sum(ballots) > (len(crowd)/2):
        return 1
    else:
        return 0

def generate_crowd(n, mean, std):
    crowd = []
    for i in range(n):
        crowd.append(np.random.normal(mean, std))
    return crowd

mean = float(input("Please give mean accuracy of the crowd"))
std = float(input("Please give the standard deviation of the accuracy"))
y1 = []
y2 = []
for i in range(3,30,2):
    print(i)
    expert_wins = 0
    crowd_wins = 0
    for j in range(10000):
        crowd = generate_crowd(i, mean, std)
        expert_wins += expert_chooses(crowd)
        crowd_wins += crowd_chooses(crowd)
    print("Expert accuracy: ", expert_wins/10000)
    y1.append(expert_wins/10000)
    print("Crowd accuracy: ", crowd_wins/10000)
    y2.append(crowd_wins/10000)

fig, ax = plt.subplots(1, 1, figsize=(6, 4))
x = [i for i in range(3,30,2)]
ax.plot(x, y1, '-', label="Expert Accuracy")
ax.plot(x, y2, '-', label="Crowd Accuracy")
ax.legend()
plt.show()
