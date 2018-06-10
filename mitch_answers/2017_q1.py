import gurobipy as gb

def main():
    # Sets
    num_compartments = ['A', 'B', 'C', 'D']
    num_packages = 15
    # Helper iterables
    C = num_compartments
    P = range(num_packages)

    # Instantiate model
    model = gb.Model('2017 Question One')

    # Data
    weights = (70, 90, 100, 110, 120, 130, 150, 180, 210, 220, 250, 280, 340, 350, 400)
    compartment_limit = 1000
    min_packages = 3

    # Variables
    placements = {c: [model.addVar(vtype=gb.GRB.BINARY) for p in P] for c in C}

    # Constraints
    # Ensure we have at least the minimum amount of packages
    model.addConstrs(gb.quicksum(placements[c][p] for p in P)
                     >= min_packages for c in C)
    # Ensure we aren't exceeding the compartment limit
    model.addConstrs(gb.quicksum(placements[c][p] * weights[p] for p in P)
                     <= compartment_limit for c in C)
    # Ensure each package is only in one compartment
    model.addConstrs(gb.quicksum(placements[c][p] for c in C) <= 1 for p in P)
    # Ensure we are placing all the packages
    model.addConstr(gb.quicksum(placements[c][p] for c in C for p in P) == num_packages)
    # Ensure compartment A weight equals compartment D
    model.addConstr(gb.quicksum(placements['A'][p] * weights[p]  for p in P)
                    == gb.quicksum(placements['D'][p] * weights[p] for p in P))
    # Ensure compartment B weight equals compartment C
    model.addConstr(gb.quicksum(placements['B'][p] * weights[p] for p in P)
                    == gb.quicksum(placements['C'][p] * weights[p] for p in P))

    # Solve model
    model.optimize()

    # Print solution
    for c in C:
        print(f'{c} has packages: {[placements[c][p].x == 1 for p in P]}')

if __name__ == '__main__':
    main()