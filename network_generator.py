import numpy as np

class Agent:
    def __init__(self, my_id, accuracy, effort, neighbors):
        self.my_id = my_id
        self.accuracy = accuracy
        self.effort = effort
        self.neighbors = neighbors
        self.delegate = my_id
        self.guru_accuracy = accuracy
        self.expected_utility = accuracy - effort

    def cast_ballot(self):
        if np.random.uniform(0,1) < self.accuracy:
            return 1
        else:
            return 0

class Network:
    def __init__(self, n_agents):
        self.agents = [Agent(i, init_acc_func(), init_eff_func(), []) for i in range(n_agents)]

    def get_mean_accuracy(self):
        accuracies = [a.guru_accuracy for a in self.agents]
        return np.mean(accuracies)

    def find_guru(self, i):
        def search_step(i, itr):
            if itr > len(self.agents):
                return -1 #ended in a cycle, there is no guru!
            d = self.agents[i].delegate
            if d == i:
                return d
            else:
                return search_step(d, itr + 1)
            
        return search_step(i, 0)

def init_acc_func():
    return np.random.normal(0.75, 0.05)

def init_eff_func():
    return 0 #np.random.normal(0.025, 0.01)

def generate_network(net_type, n_agents, degree):
    n = Network(n_agents)
    if net_type == "random":
        return generate_random(n, degree)
    elif net_type == "regular":
        return generate_regular(n, degree)
    else:
        return "TOTAL FAILURE YOU FOOL, GIVE AN ACTUAL NETWORK TYPE DUHHHH!"

def generate_random(n, degree):
    probability = degree / len(n.agents)
    for i in range(len(n.agents)):
        for j in range(i):
            if np.random.uniform(0, 1) < probability:
                n.agents[i].neighbors.append(j)
                n.agents[j].neighbors.append(i)
    return n

def generate_regular(n, degree):
    #initialize regular graph
    return n
