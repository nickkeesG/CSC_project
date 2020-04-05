import networkx
import matplotlib.pyplot as plt
import numpy as np

import voting_mechanism as vm
import network_generator as ng

def iterated_voting(n):
    has_converged = False
    total_updates = 0
    total_passes = 0
    while not has_converged:
        (n, has_converged, n_updates) = vm.sequential_update(n)
        total_passes += 1
        total_updates += n_updates
    return total_passes, total_updates

def one_shot_voting(n, n_props):
    n = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n, n_props)
    total_gurus = n.get_n_gurus()
    mean_dist_g = n.get_mean_dist_guru()
    return outcome, mean_acc, total_gurus, mean_dist_g

def plot_network(n):
    graph = networkx.DiGraph()
    for a in n.agents:
        for x in a.neighbors:
            graph.add_edge(a.my_id, x)
    position = networkx.spring_layout(graph,k=0.2,iterations=70)
    networkx.draw_networkx(graph, pos=position)
    plt.show() 

def run_experiment_oneshot(network_type, n_agents, degree, n_props, effort, iterations):
    accuracy = np.empty(iterations)
    outcomes = np.empty(iterations)
    log_n_gurus = np.empty(iterations)
    for i in range(iterations):
        n = ng.generate_network(network_type, n_agents, degree, effort)
        outcome, mean_acc, n_gurus, mean_dist_g = one_shot_voting(n, n_props)
        outcomes[i] = outcome
        accuracy[i] = mean_acc
        log_n_gurus[i] = n_gurus 
    average_accuracy = np.mean(accuracy)
    mean_n_gurus = np.mean(log_n_gurus)
    probability_correct = sum([1 for x in outcomes if x == 0]) / iterations
    mean_dist_guru = np.mean(mean_dist_g)
    return average_accuracy, probability_correct, mean_n_gurus, mean_dist_guru

def run_full_experiment_oneshot():
    n_agents = 250
    types = ["random", "regular", "caveman", "relaxed_caveman"]
    degrees = [4, 8, 12, 16, 20, 24]
    n_props = 2
    iterations = 1000
    for effort in [True, False]:
        for t in types:
            for d in degrees:
                avg_acc, prob_corr, mean_n_gurus, mean_dist_guru = run_experiment(t, n_agents, d, n_props, effort, iterations)
                print("Effort: ", effort, "\tType: ", t, "\tDegrees: ", d, "\tMean_acc: ", avg_acc, "\tProb_corr", prob_corr, "\tMean_n_gurus: ", mean_n_gurus, "\tMean_dist_guru: ", mean_dist_guru)
    
def run_full_experiment_iterated():
    n_agents = 250
    types = ["random", "regular", "caveman", "relaxed_caveman"]
    degrees = [4, 8, 12, 16, 20, 24]
    iterations = 1000
    for effort in [True, False]:
        for t in types:
            for d in degrees:
                passes = []
                updates = []
                for i in range(iterations):
                    n = ng.generate_network(t, n_agents, d, effort)
                    p, u = iterated_voting(n)
                    passes.append(p)
                    updates.append(u)
                print("Effort: ", effort, "\tType: ", t, "\tDegrees: ", d, "Passes: ", np.mean(passes), " (", np.std(passes), ") BR updates: ", np.mean(updates), " (", np.std(updates), ")") 

if __name__ == "__main__":
    run_full_experiment_iterated()
    
