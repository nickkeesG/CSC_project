import voting_mechanism as vm
import network_generator as ng

def iterated_voting(n):
    has_converged = False
    while not has_converged:
        (n, has_converged) = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n)
    return outcome, mean_acc

def one_shot_voting(n):
    (n, _) = vm.update_delegates(n)
    mean_acc = n.get_mean_accuracy()
    outcome = vm.vote(n)
    return outcome, mean_acc

if __name__ == "__main__":
    n = ng.generate_network("random", 20, 3)
    for i in range(20):
        print(i, " : ", n.agents[i].neighbors)
