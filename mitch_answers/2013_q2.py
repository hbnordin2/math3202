def main():
    # Stages
    balls = 10

    # Data
    # Number of targets
    num_targets = 4
    # Points obtained for hitting target i
    target_points = (6, 4, 10, 7)
    # Probability of missing target i given aiming at i
    target_miss = (0.8, 0.6, 0.9, 0.5)
    # Probability of hitting target i given aiming at i
    target_hit = [1 - miss for miss in target_miss]

    def get_actions():
        '''
        Generates and yields every possible action at a state. In this case,
        this is the number of bottles to order.
        '''
        for i in range(num_targets):
            yield i

    def T(state, action):
        '''
        Transition function. Returns the transition state of performing the
        given action at the given state under the given demand.
        '''
        balls_shot, target_shots = state
        target_aimed = action
        updated_shots = list(target_shots)
        updated_shots[target_aimed] += 1
        return (balls_shot + 1, tuple(updated_shots))

    def C(state, action):
        '''
        Contribution function. Returns the contribution of performing the given
        action at the given state.
        '''
        _, target_shots = state
        target_aimed = action
        probability_all_miss = target_miss[target_aimed] ** target_shots[target_aimed]
        probability_hit = target_hit[target_aimed]
        return probability_all_miss * probability_hit * target_points[target_aimed]

    def Q(state, action):
        '''
        Q Function. Returns the expected return from performing the given action
        at the given state.
        '''
        balls_shot, _ = state
        if balls_shot == balls:
            return 0
        return C(state, action) + V(T(state, action))[0]

    def V(state):
        '''
        Value function. Returns a tuple of the maximum value possible from the
        given state as well as the optimal action to take.
        '''
        if state not in values:
            values[state] = max((Q(state, a), a) for a in get_actions())
        return values[state]

    values = {}
    # State is the number of balls left and the shots we've taken at targets so far
    state = (0, tuple([0] * num_targets))
    max_points = V(state)[0]

    print(values)

    print('Optimal strategy:')
    while True:
        value, action = V(state)
        print(f'At state {state} shoot at target {action} to get value {value}')
        if state[0] == balls - 1:
            break
        state = T(state, V(state)[1])

    print(f'Max points: {max_points}')

if __name__ == '__main__':
    main()
