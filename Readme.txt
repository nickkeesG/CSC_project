All experiments with 1000 trials, 250 agents. Agent accuracy set like in Davide's report: mean=0.75, std=0.05. Effort: mean = 0.025 std=0.01
If there is no effort, effort = 0.

Mean Accuracy of the network is measured by giving each agent the accuracy of their guru, and then taking the mean. 

The maximum accuracy with 250 agents is usually about 0.89 given the mean and std used. (so the mean can't really be more than that)

More agents voting directly means a higher probability of success, because of jury theorem. If only one agent votes, then the probability of success is equal to that agent's accuracy. 

A politician is a voter which has no neighbors, but is a neighbor to all agents in the network. (all agents can delegate to the politician, but the politician cannot delegate) 


Expansions on Davide's report: 
---new network types: caveman and relaxed caveman
---Assymetric social relationships: politicians
---more than 2: implemented schultz method
