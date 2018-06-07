import gurobipy as gb

def main():
    # Sets
    ad_types = ['TV', 'Social Media', 'Print', 'Radio', 'Cinema', 'In-Store']

    # Instantiate model
    model = gb.Model('2013 Question One')

    # Data
    customers_reached = [1000000, 200000, 300000, 400000, 450000, 450000]
    costs = [500000, 150000, 300000, 250000, 250000, 100000]
    designer_hours = [700, 250, 200, 200, 300, 400]
    salesman_hours = [200, 100, 100, 100, 100, 1000]
    resources = [costs, designer_hours, salesman_hours]
    resource_limits = [1400000, 1500, 1200]

    # Variables
    # Whether we will use an advertising
    will_use = {a: model.addVar(vtype=gb.GRB.BINARY) for a in ad_types}

    # Objective
    # Maximise the number of customers reached
    model.setObjective(gb.quicksum(will_use[a] * customers_reached[i]
                                   for i, a in enumerate(ad_types)),
                       gb.GRB.MAXIMIZE)

    # Constraints
    # Ensure we do not exceed resource limits
    model.addConstrs(gb.quicksum(will_use[a] * resources[r][i]
                                 for i, a in enumerate(ad_types))
                     <= resource_limits[r]
                     for r in range(len(resources)))

    # Ensure we have at least one radio or cinema if we have an in-store campaign
    model.addConstr(will_use['Radio'] + will_use['Cinema'] >= will_use['In-Store'])

    # Ensure we are using at most one of the social media or cinema campaigns
    model.addConstr(will_use['Social Media'] + will_use['Cinema'] <= 1)

    # Solve model
    model.optimize()

    # Print solution
    for a in ad_types:
        print(f'Advertisement Type: {a}')
        print(f'Will Use: {will_use[a].x}')
    print(f'Customers Reached: {model.objVal}')

if __name__ == '__main__':
    main()