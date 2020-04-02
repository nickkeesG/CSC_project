import numpy as np
import networkx

class Agent:
    def __init__(self, my_id, accuracy, effort, neighbors):
        self.my_id = my_id
        self.accuracy = accuracy
        self.effort = effort
        self.neighbors = neighbors
        self.delegate = my_id
        self.guru_accuracy = accuracy
        self.expected_utility = accuracy - effort

    def cast_ballot(self, n_propositions): #the 0th proposition is the "correct" one
        x = self.accuracy*2 -1
        #P(rand(x,1) > rand(0,1)) = self.accuracy
        prop_values = [np.random.uniform(x,1)] + [np.random.uniform(0,1) for i in range(n_propositions -1)]
        ballot = np.argsort(prop_values)[::-1]
        return ballot

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
    if net_type == "random":
        return generate_random(n_agents, degree)
    elif net_type == "regular":
        return generate_regular(n_agents, degree)
    elif net_type == "caveman":
        return generate_caveman(n_agents, degree)
    elif net_type == "relaxed_caveman":
        return generate_relaxed_caveman(n_agents, degree)
    else:
        return "The network type given has not been found"

def generate_random(n_agents, degree):
    n = Network(n.agents)
    probability = degree / n_agents
    for i in range(n_agents):
        for j in range(i):
            if np.random.uniform(0, 1) < probability:
                n.agents[i].neighbors.append(j)
                n.agents[j].neighbors.append(i)
    return n

def generate_regular(n_agents, degree):
    n = Network(n.agents)
    graph = networkx.random_regular_graph(degree, n_agents)
    edge_list = networkx.to_edgelist(graph)
    for e in edge_list:
        n.agents[e[0]].neighbors.append(e[1])
        n.agents[e[1]].neighbors.append(e[0])
    return n

def generate_caveman(n_agents, degree):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    if not n_cliques*clique_size == n_agents:
        print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")

    n = Network(n_cliques*clique_size)    
    graph = networkx.caveman_graph(n_cliques, clique_size)
    edge_list = networkx.to_edgelist(graph)
    for e in edge_list:
        n.agents[e[0]].neighbors.append(e[1])
        n.agents[e[1]].neighbors.append(e[0])
    return n

def generate_relaxed_caveman(n_agents, degree):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    if not n_cliques*clique_size == n_agents:
        print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")
    
    n = Network(n_cliques*clique_size)
    graph = networkx.relaxed_caveman_graph(n_cliques, clique_size, 0.1) 
    edge_list = networkx.to_edgelist(graph)
    for e in edge_list:
        n.agents[e[0]].neighbors.append(e[1])
        n.agents[e[1]].neighbors.append(e[0])
    return n
