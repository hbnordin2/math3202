from gurobipy import *

m = Model("2013 Prac Exam")
m.setParam("MIPGap", 0)

# Sets
AdTypes = ["TV", "Social Media", "Print", "Radio", "Cinema", "In-store Marketing"]
Resources = ["Cost", "Designer Hours", "Salesman Hours"]

# Data
customersReached = [1000000, 200000, 300000, 400000, 450000, 450000]
costs = [500000, 150000, 300000, 250000, 250000, 100000]
designerHours = [700, 250, 200, 200, 300, 400]
salesmanHours = [200, 100, 100, 100, 100, 1000]

totalCosts = 1400000
totalDesignerHours = 1500
totalSalesmanHours = 1200

resources = [costs, designerHours, salesmanHours]
limits = [totalCosts, totalDesignerHours, totalSalesmanHours]

# Variables
X = {}
for i in AdTypes:
    X[i] = m.addVar(vtype=GRB.BINARY)

# Constraints
"""
If the In-store Marketing campaign is undertaken, it needs at least one of a Radio or a
Cinema campaign effort to support it.
"""
m.addConstr(X["In-store Marketing"] <= X["Radio"] + X["Cinema"])

"""
The firm will only use at most one of the Social Media or Cinema campaigns.
"""
m.addConstr(X["Social Media"] + X["Cinema"] <= 1)

"""
Do not exceed the resources we have
"""
for resourceIndex, resource in enumerate(Resources):
    totalResource = 0
    for adIndex, ad in enumerate(AdTypes):
        totalResource += X[ad] * resources[resourceIndex][adIndex]
    m.addConstr(totalResource <= limits[resourceIndex])

# Objective Function
totalCustomersReached = 0
for adIndex, ad in enumerate(AdTypes):
    totalCustomersReached += customersReached[adIndex] * X[ad]
m.setObjective(totalCustomersReached, GRB.MAXIMIZE)

m.optimize()

for i in AdTypes:
    print(i, X[i].x)