import numpy as np

class Agent:
    def __init__(self, my_id, accuracy, effort, neighbors):
        self.my_id = my_id
        self.accuracy = accuracy
        self.effort = effort
        self.neighbors = neighbors
        self.delegate = my_id
        self.voting_accuracy = accuracy
        self.expected_utility = accuracy - effort

    def get_accuracy(self):
        return self.voting_accuracy

class Network:
    def __init__():
        self.agents = []

    def get_mean_accuracy():
        accuracies = [a.get_accuracy() for a in self.agents]
        return np.mean(accuracies)

def generate_network(net_type):
    if net_type == "random":
        return generate_random()
    else:
        return "TOTAL FAILURE YOU FOOL, GIVE AN ACTUAL NETWORK TYPE DUHHHH!"

def generate_random():
    n = Network()
    #initialize a random network
    return n
