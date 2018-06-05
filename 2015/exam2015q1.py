from gurobipy import *
import random

m = Model("exam 2015 q1")

# 100 candidate sites
S = range(100)
random.seed(20)

# Drill cost at each site
DrillCost = [random.randint(15000,60000) for s in S]

# 30 groups with between 5 and 10 elements in every group
Group = [sorted(random.sample(S, random.randint(5,10))) for i in range(30)]
G = range(len(Group))

def yIsOneIffx1StrictlyBiggerThanx2(y, x1, x2, M):
    m.addConstr(x1 >= x2 + 1 - M*(1-y))
    m.addConstr(x2 >= x1 + 1 - M*y)

"""
Variables
"""
WellsDrilled = {}
for i in S:
    WellsDrilled[i] = m.addVar(vtype=GRB.BINARY)

GroupsDrilledTwice = {}
for i in G:
    GroupsDrilledTwice[i] = m.addVar(vtype=GRB.BINARY)

"""
Constraints
"""
# Drill 20 wells
m.addConstr(quicksum(WellsDrilled[i] for i in WellsDrilled) == 20)

# Drill at most 2 wells in each group
for groupIndex, group in enumerate(Group):
    totalDrilledInGroup = quicksum(WellsDrilled[i] for i in group)

    m.addConstr(totalDrilledInGroup <= 2)

    # GroupsDrilledTwice is 1 iff 2 wells has been drilled in that group, 0 otherwise
    # 2 -> 1
    # 1 -> 0
    # 0 -> 0
    m.addConstr(GroupsDrilledTwice[groupIndex] >= totalDrilledInGroup - 1)

"""
Objective function
"""

costOfDrills = quicksum(DrillCost[i] * WellsDrilled[i] for i in S)
costOfFines = 10000 * quicksum(GroupsDrilledTwice[i] for i in G)

m.setObjective(costOfDrills + costOfFines, GRB.MINIMIZE)

m.optimize()

for i in WellsDrilled:
    if WellsDrilled[i].x == 1:
        print(i)