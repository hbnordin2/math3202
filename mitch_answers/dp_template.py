import math

def main():
    # Stages

    # Data

    def get_actions():
        '''
        Generates and yields every possible action at a state.
        '''


    def T(state, action):
        '''
        Transition function. Returns the transition state of performing the
        given action at the given state.
        '''
        _, _ = state
        _ = action

    def C(state, action):
        '''
        Contribution function. Returns the contribution of performing the given
        action at the given state.
        '''
        contribution = 0
        _, _ = state
        _ = action

    def Q(state, action):
        '''
        Q Function. Returns the expected return from performing the given action
        at the given state.
        '''
        _, _ = state
        if _ == _:
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
    # State: something
    state = _
    min_cost = V(state)[0]

    print(values)

    print('Optimal strategy:')
    while True:
        value, action = V(state)
        print(f'At state {state} do {action}')
        if state[0] == _ - 1:
            break
        state = T(state, V(state)[1])

    print(f'Min Cost: {min_cost}')

if __name__ == '__main__':
    main()
