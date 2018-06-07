import gurobipy as gb
import random
random.seed(20)

def main():
    # Sets
    num_sites = 100
    # Helper iterable
    S = range(num_sites)

    # Instantiate model
    model = gb.Model('2015 Question One')

    # Data
    # Drill costs for each site
    drill_costs = [random.randint(15000, 60000) for _ in S]
    # 30 groups with between 5 and 10 elements in every group
    groups = [sorted(random.sample(S, random.randint(5, 10))) for i in range(30)]
    # Number of sites to choose to drill wells
    num_wells = 20
    # Penalty for two wells in one group
    two_group_penalty = 10000
    # Helper iterable
    G = range(len(groups))

    # Variables
    # Binary variable representing whether site s will be used
    sites_with_wells = {s: model.addVar(vtype=gb.GRB.BINARY) for s in S}
    # Binary variable representing whether group g has two wells in it
    groups_with_two_wells = {g: model.addVar(vtype=gb.GRB.BINARY) for g in G}

    # Objective
    model.setObjective(gb.quicksum(groups_with_two_wells[g] for g in G) * two_group_penalty
                       + gb.quicksum(sites_with_wells[s] * drill_costs[s] for s in S),
                       gb.GRB.MINIMIZE)

    # Constraints
    # Ensure that the number of sites that we will use equals the number of
    # wells we want to drill
    model.addConstr(gb.quicksum(sites_with_wells[s] for s in S) == num_wells)
    for g in G:
        wells_in_group = gb.quicksum(sites_with_wells[s] for s in groups[g])
        # Ensure that no group is exceeding the maximum amount of wells for a group
        model.addConstr(wells_in_group <= 2)
        # Ensure that we are correctly setting groups which have two wells in them
        model.addConstr(groups_with_two_wells[g] >= wells_in_group - 1)

    # Solve model
    model.optimize()

    # Print solution
    for s in S:
        print(f'Will Use: {sites_with_wells[s].x}')
    print(f'Groups: {[groups_with_two_wells[g].x for g in G]}')
    print(f'Cost: {model.objVal}')

if __name__ == '__main__':
    main()
