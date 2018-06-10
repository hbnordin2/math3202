from gurobipy import *

# Sets
Compartments = ["A", "B", "C", "D"]
Weights = range(15)

# Data
packageWeights = [70, 90, 100, 110, 120, 130, 150, 180, 210, 220, 250, 280, 340, 350, 400]
minAllocation = 3
maxWeight = 1000

m = Model()

# Variables
X = {}
for weight in Weights:
    for compartment in Compartments:
        X[weight, compartment] = m.addVar(vtype=GRB.BINARY)

# Objective
# We don't need one

# Constraints
totalWeights = {"A":0, "B":0, "C":0, "D":0}
totalPackages = {"A":0, "B":0, "C":0, "D":0}
for compartment in Compartments:
    for i in X:
        if i[1] == compartment:
            totalWeights[compartment] += X[i] * packageWeights[i[0]]
            totalPackages[compartment] += X[i]

    # Max weight is 1000 kg
    m.addConstr(totalWeights[compartment] <= 1000)
    # We need at least 3 weights on each
    m.addConstr(totalPackages[compartment] >= 3)

# Weight of A must equal Weight of D and Weight B must equal Weight C
m.addConstr(totalWeights["A"] == totalWeights["D"])
m.addConstr(totalWeights["C"] == totalWeights["B"])

# Every weight must be placed exactly once
for weight in Weights:
    totalTimesWeightPlaced = 0
    for i in X:
        if i[0] == weight:
            totalTimesWeightPlaced += X[i]
    m.addConstr(totalTimesWeightPlaced == 1)

m.optimize()

for i in X:
    print(i, X[i].x)