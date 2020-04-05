import numpy as np
import networkx

class Agent:
    def __init__(self, my_id, accuracy, effort, neighbors):
        self.my_id = my_id
        self.accuracy = accuracy
        self.effort = effort
        self.neighbors = neighbors
        self.delegate = my_id
        self.expected_utility = accuracy - effort

    def cast_ballot(self, n_propositions): #the 0th proposition is the "correct" one
        x = self.accuracy*2 -1
        #P(rand(x,1) > rand(0,1)) = self.accuracy
        prop_values = [np.random.uniform(x,1)] + [np.random.uniform(0,1) for i in range(n_propositions -1)]
        ballot = np.argsort(prop_values)[::-1]
        return ballot

class Network:
    def __init__(self, n_agents, effort):
        self.agents = [Agent(i, init_acc_func(), init_eff_func(effort), []) for i in range(n_agents)]
        for i in range(len(self.agents)):
            np.random.shuffle(self.agents[i].neighbors)

    def get_mean_accuracy(self):
        guru_accuracies = [0.5 for i in range(len(self.agents))]
        for i in range(len(self.agents)):
            g = self.find_guru(i)
            if not g == -1:
                guru_accuracies[i] = self.agents[g].accuracy
        return np.mean(guru_accuracies)

    def get_n_gurus(self):
        total_gurus = 0
        for a in self.agents:
            if a.my_id == a.delegate:
                total_gurus += 1
        return total_gurus

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

    def create_politicians(self, n_politicians):
        politicians = np.random.choice(len(self.agents), n_politicians)
        for p in politicians:
            self.agents[p].neighbors = []
            for i in range(len(self.agents)):
                if not i in politicians:
                    if not p in self.agents[i].neighbors:
                        self.agents[i].neighbors.append(p)

def init_acc_func():
    return np.random.normal(0.75, 0.05)

def init_eff_func(effort):
    if effort:
        return np.random.normal(0.025, 0.01)
    else:
        return 0

def graph_to_net(n_agents, graph, effort):
    n = Network(n_agents, effort)
    edge_list = networkx.to_edgelist(graph)
    for e in edge_list:
        n.agents[e[0]].neighbors.append(e[1])
    return n

def generate_network(net_type, n_agents, degree, effort):
    if net_type == "random":
        return generate_random(n_agents, degree, effort)
    elif net_type == "regular":
        return generate_regular(n_agents, degree, effort)
    elif net_type == "caveman":
        return generate_caveman(n_agents, degree, effort)
    elif net_type == "relaxed_caveman":
        return generate_relaxed_caveman(n_agents, degree, effort)
    else:
        print("The network type given has not been found")
        exit()

def generate_random(n_agents, degree, effort):
    n = Network(n_agents, effort)
    probability = degree / n_agents
    for i in range(n_agents):
        for j in range(i):
            if np.random.uniform(0, 1) < probability:
                n.agents[i].neighbors.append(j)
                n.agents[j].neighbors.append(i)
    return n

def generate_regular(n_agents, degree, effort):
    graph = networkx.random_regular_graph(degree, n_agents)
    graph = graph.to_directed()
    n = graph_to_net(n_agents, graph, effort)
    return n

def generate_caveman(n_agents, degree, effort):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    #if not n_cliques*clique_size == n_agents:
    #    print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")
    
    graph = networkx.caveman_graph(n_cliques, clique_size) 
    graph = graph.to_directed()
    n = graph_to_net(n_cliques*clique_size, graph, effort)
    return n

def generate_relaxed_caveman(n_agents, degree, effort):
    clique_size = degree + 1
    n_cliques = int(n_agents/clique_size)
    #if not n_cliques*clique_size == n_agents:
    #    print("Warning, size= ", str(n_cliques*clique_size), " being used for caveman graph")
    
    graph = networkx.relaxed_caveman_graph(n_cliques, clique_size, 0.2)    
    graph = graph.to_directed()
    n = graph_to_net(n_cliques*clique_size, graph, effort)
    return n
