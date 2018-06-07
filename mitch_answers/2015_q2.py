import math

def main():
    # Stages
    seasons = 5

    # Data
    operators_required = [155, 120, 140, 100, 155]
    excess_employment_cost = 2000
    delta_multiplier = 200

    def get_actions():
        '''
        Generates and yields every possible action at a state. In this case,
        this is the number of bottles to order.
        '''
        max_fire = max(operators_required) - min(operators_required)
        max_hire = max(operators_required)
        for i in range(-max_fire, max_hire + 1):
            yield i

    def T(state, action):
        '''
        Transition function. Returns the transition state of performing the
        given action at the given state under the given demand.
        '''
        season, operators_hired = state
        delta_hired = action
        return (season + 1, operators_hired + delta_hired)

    def C(state, action):
        '''
        Contribution function. Returns the contribution of performing the given
        action at the given state.
        '''
        contribution = 0
        season, operators_hired = state
        delta_hired = action
        current_hired = operators_hired + delta_hired
        if current_hired < operators_required[season]:
            return math.inf
        excess_hired = abs(current_hired - operators_required[season])
        contribution += excess_hired * excess_employment_cost
        contribution += delta_multiplier * abs(delta_hired) ** 2
        return contribution

    def Q(state, action):
        '''
        Q Function. Returns the expected return from performing the given action
        at the given state.
        '''
        season, _ = state
        if season == seasons:
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
    # State: (season, current number of operators)
    state = (0, 0)
    min_cost = V(state)[0]

    print(values)

    print('Optimal strategy:')
    while True:
        value, action = V(state)
        print(f'At state {state} hire {action} operators to get value {value}')
        if state[0] == seasons - 1:
            break
        state = T(state, V(state)[1])

    print(f'Min Cost: {min_cost}')

if __name__ == '__main__':
    main()
