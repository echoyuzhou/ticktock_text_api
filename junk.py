import random
def action_selection(self,state):
    q =[self.getQ(state,a] for a in self.actions]
    maxQ = max(q)
    if random.random()< self.epsilon:
        best = [i for i in range(len(self.actions))if q[i]==maxQ]
        index = random.choice(best)
    else:
        index = q.index(maQ)
    action = self.actions[index]
return action
