import math
import random

def main():
    # Stages
    num_boxes = 4

    # Data
    num_cards = 10

    def get_actions():
        '''
        Generates and yields every possible action at a state.
        '''
        for box_to_fill in range(num_boxes):
            yield box_to_fill

    def get_transition_states(state, action):
        '''
        Generates and yields every possible transition state at a given state
        when performing the given action.
        '''
        _, _, cards_left, _ = state
        transitional_probability = 1 / len(cards_left)
        for new_card_drawn in cards_left:
            yield transitional_probability, T(state, action, new_card_drawn)

    def T(state, action, new_card_drawn):
        '''
        Transition function. Returns the transition state of performing the
        given action at the given state.
        '''
        boxes_filled, card_drawn, cards_left, boxes = state
        box_to_fill = action
        new_boxes = tuple([card_drawn if i == box_to_fill else box
                           for i, box in enumerate(boxes)])
        new_cards_left = frozenset([card for card in cards_left
                                    if card != new_card_drawn])
        return (boxes_filled + 1, new_card_drawn, new_cards_left, new_boxes)

    def C(state, action):
        '''
        Contribution function. Returns the contribution of performing the given
        action at the given state.
        '''
        boxes_filled, card_drawn, _, boxes = state
        box_to_fill = action
        # If we haven't filled all the boxes yet
        if boxes_filled < num_boxes - 1:
            return 0
        new_boxes = tuple([card_drawn if i == box_to_fill else box
                           for i, box in enumerate(boxes)])
        top = new_boxes[0] * 10 + new_boxes[1]
        bottom = new_boxes[2] * 10 + new_boxes[3]
        return top * bottom

    def Q(state, action):
        '''
        Q Function. Returns the expected return from performing the given action
        at the given state.
        '''
        boxes_filled, _, _, boxes = state
        box_to_fill = action
        if boxes_filled == num_boxes:
            return 0
        if boxes[box_to_fill] is not None:
            return math.inf
        return C(state, action) \
               + sum(transition_probability * V(transition_state)[0]
                     for transition_probability, transition_state
                     in get_transition_states(state, action))

    def V(state):
        '''
        Value function. Returns a tuple of the maximum value possible from the
        given state as well as the optimal action to take.
        '''
        if state not in values:
            values[state] = min((Q(state, a), a) for a in get_actions())
        return values[state]






    # Beware, junk below.






    values = {}
    # State: (boxes_filled: int, card_drawn: int, cards_left: set[int], boxes: List[int])
    for initial_draw in range(num_cards):
        initial_cards = frozenset([i for i in range(num_cards) if i != initial_draw])
        initial_state = (0, initial_draw, initial_cards, tuple([None] * num_boxes))
        print('Min cost:', V(initial_state)[0])

    # Play random game
    print('Starting random game')
    random_draw = random.sample(list(range(num_cards)), 1)[0]
    print(f'Drew {random_draw}')
    cards_left = frozenset([i for i in range(num_cards) if i != random_draw])
    state = (0, random_draw, cards_left, tuple([None] * num_boxes))
    while True:
        value, action = V(state)
        _, _, cards_left, boxes = T(state, action, random_draw)
        print(f'Best to place {random_draw} in box {action} to get {boxes}')
        random_draw = random.sample(cards_left, 1)[0]
        state = T(state, action, random_draw)
        if state[0] == num_boxes:
            break
        print(f'Drew {random_draw}')
    print(f'Final cost: {value}')

if __name__ == '__main__':
    main()
