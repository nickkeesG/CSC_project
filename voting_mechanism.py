import numpy as np
import itertools
import random

class Tournament:
    def __init__(self, n_props):
        # counts the support for a over b [a, b]
        self.matrix = np.zeros((n_props, n_props))
        self.props_remaining = {i for i in range(n_props)}

    def count_ballot(self, ballot, weight):
        for i in range(len(ballot)):
            for j in range(i+1, len(ballot)):
                self.matrix[ballot[i], ballot[j]] += weight
    
    def find_schwartz_set(self):
        for i in range(1, len(self.props_remaining)+1):
            subsets = list(itertools.combinations(self.props_remaining, i))
            schwartz_sets = []
            for s in subsets:
                if self.is_schwartz_set(s):
                    schwartz_sets.append(s)
            if len(schwartz_sets) > 0:
                return random.choice(schwartz_sets) #see README for justication of tiebreaking
        print("no schwartz set (you fucked up!)")
        return {}

    def is_schwartz_set(self, subset):
        for p1 in subset:
            for p2 in [p for p in list(self.props_remaining) if not p in subset]:
                if self.matrix[p2, p1] > self.matrix[p1, p2]:
                    return False
        return True

    def delete_weakest_edge(self):
        weakest_edge = []
        weakest_strength = 99999999999
        for i in self.props_remaining:
            for j in self.props_remaining:
                if i > j:
                    if not self.matrix[i,j] == self.matrix[j,i]:
                       strength = max(self.matrix[i,j], self.matrix[j,i])
                       if strength < weakest_strength:
                           weakest_strength = strength
                           weakest_edge = [(i, j)]
                       elif strength == weakest_strength:
                           weakest_edge.append((i, j))
        edge = random.choice(weakest_edge)
        self.matrix[edge[0], edge[1]] = 0
        self.matrix[edge[1], edge[0]] = 0

    def find_winner(self): #Schultze method
        self.props_remaining = self.find_schwartz_set()
        if len(self.props_remaining) == 1:
            return list(self.props_remaining)[0]
        self.delete_weakest_edge()
        self.find_winner()

#sequentially update agents
def sequential_update(n):
    old_profile = [n.agents[i].delegate for i in range(len(n.agents))]
    order = [i for i in range(len(n.agents))] 
    np.random.shuffle(order)
    for i in order:
        d = i
        best_utility = n.agents[i].accuracy - n.agents[i].effort

        for j in n.agents[i].neighbors:
            n.agents[i].delegate = j
            g = n.find_guru(i)
            if not g == -1 and n.agents[g].accuracy > best_utility:
                best_utility = n.agents[g].accuracy
                d = j
        n.agents[i].delegate = d

    n_updates = 0
    for i in range(len(n.agents)):
        if not n.agents[i].delegate == old_profile[i]:
            n_updates += 1
    return n, n_updates == 0, n_updates

#update all agents simultaneously
def update_delegates(n):
    delegation_profile = [n.agents[i].delegate for i in range(len(n.agents))]
    for i in range(len(n.agents)):
        best_utility = n.agents[i].accuracy - n.agents[i].effort

        for j in n.agents[i].neighbors:
            if n.agents[j].accuracy > best_utility:
                best_utility = n.agents[j].accuracy
                delegation_profile[i] = j
    
    #update the delegations of all agents
    for i in range(len(n.agents)):
        n.agents[i].delegate = delegation_profile[i]
    return n

def vote(n, n_props):
    #delegate step
    guru_weights = [0 for i in range(len(n.agents))]
    for i in range(len(n.agents)):
        g = n.find_guru(i)
        if not g == -1: #g == -1 in the case of no guru being found (ie a cycle)
            guru_weights[g] += 1
    
    #vote step
    t = Tournament(n_props)
    for i in range(len(n.agents)):
        ballot = n.agents[i].cast_ballot(n_props)
        t.count_ballot(ballot, guru_weights[i])
    return t.find_winner()
