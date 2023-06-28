import numpy as np
from typing import List,Any, Dict, Tuple, Union
import random

def softmax(d:dict):
    n = 0
    vs = [d[k] for k in d]
    m = min(vs)
    for k,v in d.items():
        d[k] = np.exp(20*(v-m))
        n += d[k]
    for k in d:
        d[k] /= n
    return d

def random_proceed(scoreboard, p1, p2, goal1, goal2):
    if goal1 == 0:
        return True
    elif goal2 == 0:
        return False
    
    deck1 = random.choice(p1)
    deck2 = random.choice(p2)
    
    wr = scoreboard[deck1, deck2]
    if random.random() < wr:
        np1 = [deck for deck in p1 if deck != deck1]
        np2 = p2
        return random_proceed(scoreboard, np1,np2, goal1 - 1, goal2)
    else:
        np1 = p1
        np2 = [deck for deck in p2 if deck != deck2]
        return random_proceed(scoreboard, np1,np2, goal1, goal2 - 1)

def rollout(scoreboard,p1,p2, goal1, goal2, N = 1):
    #print(p1,p2)
    assert len(p1) >= goal1
    assert len(p2) >= goal2
    wins = 0
    for i in range(N):
        if random_proceed(scoreboard, p1,p2, goal1, goal2):
            wins += 1
    return wins / N

class PickHelper:
    def __init__(self, scoreboard) -> None:
        self.sb = scoreboard
        pass
    def pick(self, p1:List[int], p2:List[int], g1, g2, N = 2000)->Dict[int, float]:
        """
        p1,p2:可选卡组列表(下标)
        gx:x的目标胜场.
        
        返回抽选某个卡组的概率.
        """
        ##这么传是因为helper可以进行一些剪枝优化(前面搜过的状态直接复用)
        vals = {deck:0 for deck in p1}
        for deck in vals:
            recs = []
            np1 = [k for k in p1 if k != deck]
            for rival in p2:
                np2 = [k for k in p2 if k!= rival]
                wr = self.sb[deck,rival]
                recs.append(wr * rollout(self.sb,np1,p2,g1-1,g2,N) +
                            (1-wr)* rollout(self.sb,p1,np2,g1,g2-1,N))
            vals[deck] = sum(recs)/len(recs)
        #n = 0
        #for _, val in vals.items():
        #    n += val
        #for k in vals:
        #    vals[k] = vals[k] / n
        #return vals
        n = 0
        for _, val in vals.items():
            n += val
        print("胜率:", n/len(vals))
        return softmax(vals)
    def profit(self, p1, p2, g1,g2, N):
        vals = {deck:0 for deck in p1}
        for deck in vals:
            recs = []
            np1 = [k for k in p1 if k != deck]
            for rival in p2:
                #print("p2=",p2)
                np2 = [k for k in p2 if k!= rival]
                wr = self.sb[deck,rival]
                recs.append(wr * rollout(self.sb,np1,p2,g1-1,g2,N) +
                            (1-wr) * rollout(self.sb, p1,np2,g1,g2-1,N))
            vals[deck] = sum(recs)/len(recs)
        n = 0.0
        for _, val in vals.items():
            n += val
        return n/len(vals)

class BanHelper:
    def __init__(self,scoreboard) -> None:
        self.sb = scoreboard
        pass
    def predict(self, goal, N):
        picker = PickHelper(self.sb)
        p1 = list(range(len(self.sb)))
        p2 = [k for k in p1]
        vals = {}
        for candidate in p2:
            np2 = [k for k in p2 if k != candidate]
            value = 0.0
            for deck in p1:
                np1 = [k for k in p1 if k != deck]
                value += picker.profit(np1,np2,goal,goal, N)
            value = value/len(p1)
            vals[candidate] = value
        return vals
    def ban(self, goal, N):
        """
        返回ban掉**对方**的卡组概率
        """
        picker = PickHelper(self.sb)
        p1 = list(range(len(self.sb)))
        p2 = [k for k in p1]
        vals = {}
        for candidate in p2:
            np2 = [k for k in p2 if k != candidate]
            value = 0.0
            for deck in p1:
                np1 = [k for k in p1 if k != deck]
                value += picker.profit(np1,np2,goal,goal, N)
            value = value/len(p1)
            vals[candidate] = value
        n = 0
        for _, val in vals.items():
            n += np.exp(val)
        #print(vals)
        for k in vals:
            vals[k] = np.exp(vals[k]) / n
        return vals
        
                