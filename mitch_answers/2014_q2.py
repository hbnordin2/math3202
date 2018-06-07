import math

def main():
    # Stages
    months = 6

    # Data
    demand = [10, 20, 30, 30, 20, 20]
    transfer_cost = 0.1
    stock_limit = 40
    order_cost = 20
    unit_cost = 2
    order_limit = 60
    order_step = 10

    def get_actions():
        '''
        Generates and yields every possible action at a state. In this case,
        this is the number of bottles to order.
        '''
        for i in range(0, order_limit + 1, order_step):
            yield i

    def total_order_cost(units_ordered):
        '''
        Returns the cost of ordering the given the number of units.
        '''
        if units_ordered == 0:
            return 0
        return order_cost + units_ordered * unit_cost

    def T(state, action):
        '''
        Transition function. Returns the transition state of performing the
        given action at the given state under the given demand.
        '''
        month, units_stocked = state
        units_ordered = action
        units_remaining = units_stocked + units_ordered - demand[month]
        units_transfered = min(stock_limit, units_remaining)
        return (month + 1, units_transfered)

    def C(state, action):
        '''
        Contribution function. Returns the contribution of performing the given
        action at the given state.
        '''
        contribution = 0
        month, units_stocked = state
        units_ordered = action
        units_remaining = units_stocked + units_ordered - demand[month]
        if units_remaining < 0:
            return math.inf
        units_transfered = min(stock_limit, units_remaining)
        contribution += units_transfered * transfer_cost
        contribution += total_order_cost(units_ordered)
        return contribution

    def Q(state, action):
        '''
        Q Function. Returns the expected return from performing the given action
        at the given state.
        '''
        month, _ = state
        if month == months:
            return 0
        return C(state, action) + V(T(state, action))[0]

    def V(state):
        '''
        Value function. Returns a tuple of the maximum value possible from the
        given state as well as the optimal action to take.
        '''
        if state not in values:
            values[state] = min((Q(state, a), a) for a in get_actions())
        return values[state]

    values = {}
    # State is the current month and amount of stock on-hand
    state = (0, 0)
    min_cost = V(state)[0]
    print(values)
    print(f'Min cost: {min_cost}')

if __name__ == '__main__':
    main()
