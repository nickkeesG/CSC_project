import networkx
import matplotlib.pyplot as plt

import voting_mechanism as vm
import network_generator as ng

def iterated_voting(n, n_props):
    has_converged = False
    while not has_converged:
        (n, has_converged) = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n, n_props)
    return outcome, mean_acc

def one_shot_voting(n):
    (n, _) = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n)
    return outcome, mean_acc

def plot_network(n):
    graph = networkx.Graph()
    for a in n.agents:
        for x in a.neighbors:
            graph.add_edge(a.my_id, x)
    networkx.draw_networkx(graph)
    plt.show() 

if __name__ == "__main__":
    n = ng.generate_network("gaussian_partition", 40, 3)
    plot_network(n)

    print(iterated_voting(n, 6))
