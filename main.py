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
    n = ng.generate_network("regular", 20, 3)
    for a in n.agents:
        print(a.neighbors)
    print(iterated_voting(n))
