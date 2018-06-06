from gurobipy import *
import random

# Data and ranges
nHospitalSites = 30
nSuburbs = 55
MaxSuburbsPerHospital = 7
MaxPopulation = 500000

# Hospital names
H = range(nHospitalSites)
# Suburb names
S = range(nSuburbs)

random.seed(3)

# Cost of building each hospital
FixedCost = [random.randint(5000000,10000000) for h in H]
# Amount of population in each suburb
Population = [random.randint(60000,90000) for s in S]

# Travel distance - multiply by population moved to get travel cost
# Dist[hospitalName][suburbName]
Dist = [[random.randint(0,50) for s in S] for h in H]

# Set up model and set the gap on the answer to 0
m = Model()
m.setParam('MIPGap', 0)

def yIsOneIffx1StrictlyBiggerThanx2(y, x1, x2, M):
    m.addConstr(x1 >= x2 - M*(1-y) + 1)
    m.addConstr(x2 >= x1 - M*y)

def castToBoolean(y, x, U):
    m.addConstr(y <= x)
    m.addConstr(x <= U * y)

"""
Variables
"""
# 1 iff suburb is assigned to hospital
suburbToHospital = {}
for suburbName in S:
    for hospitalName in H:
        suburbToHospital[suburbName, hospitalName] = m.addVar(vtype=GRB.BINARY)

# 1 iff we are building the hospital
hospitals = {}
for hospitalName in H:
    hospitals[hospitalName] = m.addVar(vtype=GRB.BINARY)

"""
Constraints
"""

for h in H:
    totalPopulation = 0
    totalServing = 0
    for suburbName, hospitalName in suburbToHospital:
        if hospitalName == h:
            totalServing += suburbToHospital[suburbName, hospitalName]
            totalPopulation += suburbToHospital[suburbName, hospitalName] * Population[suburbName]
 
    # No hospital can serve more than 7 suburbs
    m.addConstr(totalPopulation <= 500000)
    # No hospital can serve more than 500,000 people
    m.addConstr(totalServing <= 7)

    # Hospitals is only 1 iff there's a suburb in it
    yIsOneIffx1StrictlyBiggerThanx2(hospitals[h], totalServing, 0, 1000)

# Make sure a suburb is only allocated to 1 hospital
for i in S:
    numberOfHospitalSuburbHasBeenAllocatedTo = 0
    for suburbName, hospitalName in suburbToHospital:
        if i == suburbName:
            numberOfHospitalSuburbHasBeenAllocatedTo += suburbToHospital[suburbName, hospitalName]
    m.addConstr(numberOfHospitalSuburbHasBeenAllocatedTo == 1)

"""
Objective function
"""
costOfBuilding = 0
for h in H:
    costOfBuilding += FixedCost[h] * hospitals[h]

costOfTransport = 0
for h in H:
    for s in S:
        costOfTransport += suburbToHospital[s, h] * Dist[h][s]

totalCost = costOfBuilding + costOfTransport

m.setObjective(totalCost, GRB.MINIMIZE)

m.optimize()

for i in hospitals:
    if hospitals[i].x == 1:
        print(i)