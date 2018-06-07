import gurobipy as gb
import random
random.seed(3)

def main():
    # Sets
    num_hospitals = 30
    num_suburbs = 55
    # Helper iterables
    H = range(num_hospitals)
    S = range(num_suburbs)

    # Instantiate model
    model = gb.Model('2016 Question One')
    model.setParam('MIPGap', 0)

    # Data
    max_suburbs_per_hospital = 7
    max_population_per_hospital = 500000
    # Travel distance for each hospital to each suburb
    # Construction cost for each hospital
    construction_costs = [random.randint(5000000, 10000000) for h in H]
    # Population of each suburb
    populations = [random.randint(60000, 90000) for s in S]
    # Note: Multiply by amount of population moved to get travel cost
    distances = [[random.randint(0, 50) for s in S] for h in H]

    # Variables
    # Boolean variable representing whether we will build hospital h
    will_build = [model.addVar(vtype=gb.GRB.BINARY) for h in H]
    # Boolean variable representing whether suburb s is assigned to hospital h
    assigned = [[model.addVar(vtype=gb.GRB.BINARY) for s in S] for h in H]

    # Objective
    # Minimise the cost of building hospitals and the cost of transporting
    # patients to and from hospitals
    model.setObjective(gb.quicksum(will_build[h] * construction_costs[h] for h in H)
                       + gb.quicksum(assigned[h][s] * distances[h][s] * populations[s]
                                     for s in S for h in H),
                       gb.GRB.MINIMIZE)

    # Constraints
    # Ensure if we're assigning a suburb to a hospital, that that hospital is
    # being built.
    model.addConstrs(gb.quicksum(assigned[h][s] for s in S)
                    <= max_suburbs_per_hospital * will_build[h]
                    for h in H)
    # Ensure we are only assigning each suburb to exactly one hospital
    model.addConstrs(gb.quicksum(assigned[h][s] for h in H) == 1 for s in S)
    # Ensure we aren't exceeding the maximum number of suburbs per hospital
    model.addConstrs(gb.quicksum(assigned[h][s] for s in S)
                     <= max_suburbs_per_hospital for h in H)
    # Ensure we aren't exceeding the maximum population per hospital
    model.addConstrs(gb.quicksum(assigned[h][s] * populations[s] for s in S)
                     <= max_population_per_hospital for h in H)

    # Solve model
    model.optimize()

    # Print solution
    # Print whether hospital h will be built and which suburbs are assigned to it
    for h in H:
        if will_build[h].x <= 0:
            continue
        suburbs = [s for s in S if assigned[h][s].x > 0]
        print(f'Building hospital #{h} and assigning suburbs: {suburbs}')
    print(f'Cost: {model.objVal}')

if __name__ == '__main__':
    main()
