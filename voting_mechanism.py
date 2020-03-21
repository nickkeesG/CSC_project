def update_delegates(n):
    delegation_profile = [i for i in range(len(n.agents))]
    for i in range(len(n.agents)):
        best_utility = n.agents[i].accuracy - n.agents[i].effort
        for j in n.agents[i].neighbors:
            g = n.find_guru(j)
            if n.agents[g].accuracy > best_utility:
                best_utility = n.agents[g].accuracy
                delegation_profile[i] = j
    for i in range(len(n.agents)):
        n.agents[i].delegate = delegation_profile[i]
        g = n.find_guru(i)
        if not g == -1:
            n.agents[i].voting_accuracy = n.agents[g].accuracy
        else:
            n.agents[i].voting_accuracy = 0.5
    return n

def vote(n):
    
    return 1
