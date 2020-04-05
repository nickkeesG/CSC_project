import networkx
import matplotlib.pyplot as plt
import numpy as np

import voting_mechanism as vm
import network_generator as ng

def iterated_voting(n, n_props):
    has_converged = False
    while not has_converged:
        (n, has_converged) = vm.sequential_update(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n, n_props)
    total_gurus = n.get_n_gurus()
    return outcome, mean_acc, total_gurus

def one_shot_voting(n):
    n = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n)
    return outcome, mean_acc

def plot_network(n):
    graph = networkx.DiGraph()
    for a in n.agents:
        for x in a.neighbors:
            graph.add_edge(a.my_id, x)
    position = networkx.spring_layout(graph,k=0.2,iterations=70)
    networkx.draw_networkx(graph, pos=position)
    plt.show() 

def run_experiment(network_type, n_agents, degree, n_props, effort, iterations):
    accuracy = np.empty(iterations)
    outcomes = np.empty(iterations)
    log_n_gurus = np.empty(iterations)
    for i in range(iterations):
        n = ng.generate_network(network_type, n_agents, degree, effort)
        outcome, mean_acc, n_gurus = iterated_voting(n, n_props)
        outcomes[i] = outcome
        accuracy[i] = mean_acc
        log_n_gurus[i] = n_gurus 
    average_accuracy = np.mean(accuracy)
    mean_n_gurus = np.mean(log_n_gurus)
    probability_correct = sum([1 for x in outcomes if x == 0]) / iterations
    return average_accuracy, probability_correct, mean_n_gurus

def run_full_experiment():
    n_agents = 250
    types = ["random", "regular", "caveman", "relaxed_caveman"]
    degrees = [1, 2, 3, 4, 5, 6]
    n_props = 2
    iterations = 200
    for effort in [True, False]:
        for t in types:
            for d in degrees:
                avg_acc, prob_corr, mean_n_gurus = run_experiment(t, n_agents, d, n_props, effort, iterations)
                print("Effort: ", effort, "\tType: ", t, "\tDegrees: ", d, "\tMean_acc: ", avg_acc, "\tProb_corr", prob_corr, "\tMean_n_gurus: ", mean_n_gurus) 
    

if __name__ == "__main__":
    run_full_experiment()
    
