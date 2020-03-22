def update_delegates(n):
    delegation_profile = [n.agents[i].delegate for i in range(len(n.agents))]
    for i in range(len(n.agents)):
        #get the utility of the current delegation
        current_guru = n.find_guru(i)
        if current_guru == -1:
            best_utility = 0.5
        else:
            best_utility = n.agents[current_guru].accuracy

        #switch to yourself if there is more utility
        if n.agents[i].accuracy - n.agents[i].effort > best_utility:    
            best_utility = n.agents[i].accuracy - n.agents[i].effort
            delegation_profile[i] = i
        
        #switch to a neighbor if there is more utility
        for j in n.agents[i].neighbors:
            g = n.find_guru(j)
            if not g == -1 and n.agents[g].accuracy > best_utility:
                best_utility = n.agents[g].accuracy
                delegation_profile[i] = j

    has_converged = True
    for i in range(len(n.agents)):
        if not n.agents[i].delegate == delegation_profile[i]:
            has_converged = False
            break
    
    #update the delegations of all agents
    for i in range(len(n.agents)):
        n.agents[i].delegate = delegation_profile[i]
        g = n.find_guru(i)
        if not g == -1: #g == -1 in the case of no guru being found (ie a cycle)
            n.agents[i].guru_accuracy = n.agents[g].accuracy
        else:
            n.agents[i].guru_accuracy = 0.5
    
    return n, has_converged

def vote(n):
    #delegate step
    guru_weights = [0 for i in range(len(n.agents))]
    for i in range(len(n.agents)):
        g = n.find_guru(i)
        if not g == -1: #g == -1 in the case of no guru being found (ie a cycle)
            guru_weights[g] += 1
    
    #vote step
    total_support = [0, 0]
    for i in range(len(n.agents)):
        ballot = n.agents[i].cast_ballot()
        total_support[ballot] += guru_weights[i] #agents cast with the weight of all who delegated to them

    if total_support[1] > total_support[0]:
        return 1
    else:
        return 0
