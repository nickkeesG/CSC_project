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

def graph_to_net(n_agents, graph):
    n = Network(n_agents)
    edge_list = networkx.to_edgelist(graph)
    for e in edge_list:
        n.agents[e[0]].neighbors.append(e[1])
    return n

def generate_network(net_type, n_agents, degree):
    if net_type == "random":
        return generate_random(n_agents, degree)
    elif net_type == "regular":
        return generate_regular(n_agents, degree)
    elif net_type == "caveman":
        return generate_caveman(n_agents, degree)
    elif net_type == "relaxed_caveman":
        return generate_relaxed_caveman(n_agents, degree)
   # elif net_type == "gaussian_partition":
   #     return generate_gaussian_partition(n_agents, degree)
   # elif net_type == "nuclear_families":
   #     return generate_nuclear_families(n_agents, degree)
    else:
        print("The network type given has not been found")
        exit()

def generate_random(n_agents, degree):
    n = Network(n_agents)
    probability = degree / n_agents
    for i in range(n_agents):
        for j in range(i):
            if np.random.uniform(0, 1) < probability:
                n.agents[i].neighbors.append(j)
                n.agents[j].neighbors.append(i)
    return n

def generate_regular(n_agents, degree):
    graph = networkx.random_regular_graph(degree, n_agents)
    graph = graph.to_directed()
    n = graph_to_net(n_agents, graph)
    return n

def generate_caveman(n_agents, degree):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    if not n_cliques*clique_size == n_agents:
        print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")
    
    graph = networkx.caveman_graph(n_cliques, clique_size) 
    graph = graph.to_directed()
    n = graph_to_net(n_cliques*clique_size, graph)
    return n

def generate_relaxed_caveman(n_agents, degree):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    if not n_cliques*clique_size == n_agents:
        print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")
    
    n = Network(n_cliques*clique_size)
    graph = networkx.relaxed_caveman_graph(n_cliques, clique_size, 0.2)    
    graph = graph.to_directed()
    n = graph_to_net(n_cliques*clique_size, graph)
    return n

#TODO fix degree math
#def generate_gaussian_partition(n_agents, degree):
#    p_in = 0.8
#    mean_size = degree + 1
#    if n_agents - degree - 1 <= 0 or degree*(1-p_in) < 0:
#        print("Error in gaussian partition")
#        exit()
#    size_variance = 1
#    p_out = degree*(1-p_in) / (n_agents - degree - 1) * 0.5
#    
#    graph= networkx.gaussian_random_partition_graph(n_agents, mean_size, size_variance, p_in, p_out).to_undirected()
#    graph = graph.to_directed()
#    n = graph_to_net(n_agents, graph)
#    return n
#
#def generate_nuclear_families(n_agents, degree):
#    mean_size = 4
#    p_in = 1
#    if mean_size-1 > degree or n_agents < mean_size:
#        print("Error in nuclear families")
#        exit()
#    p_out = (degree - (mean_size-1)) / (n_agents-mean_size) * 0.5
#    size_variance = 0.5
#
#    graph = networkx.gaussian_random_partition_graph(n_agents, mean_size, size_variance, p_in, p_out).to_undirected()
#    graph = graph.to_directed()
#    n = graph_to_net(n_agents, graph)
#    return n  

