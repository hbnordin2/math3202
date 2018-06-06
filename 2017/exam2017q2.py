memoize = {}

def val(card, cardsLeft, cardsPlaced):
    """
    global depth
    print(card, cardsLeft, cardsPlaced)
    depth += 1
    if depth == 200:
        exit()
    """

    # Get where you can put cards
    emptyIndices = []
    for ind, i in enumerate(cardsPlaced):
        if i == -1:
            emptyIndices.append(ind)

    # If you're on the last card, just put it down and finish
    if len(emptyIndices) == 1:
        newCardsPlaced = [j for j in cardsPlaced]
        newCardsPlaced[emptyIndices[0]] = card

        tops = 10 * newCardsPlaced[0] + newCardsPlaced[1]
        bottoms = 10 * newCardsPlaced[2] + newCardsPlaced[3]

        return tops * bottoms

    # This is just the memoize stuff
    key = (card, str(cardsLeft), str(cardsPlaced))
    if key in memoize:
        return memoize[key][0]

    # Take the card you drew out of the pack of cards left
    newCardsLeft = [i for i in cardsLeft]
    newCardsLeft.remove(card)

    assert len(newCardsLeft) + 1 == len(cardsLeft)
    assert card not in newCardsLeft

    # Get the value of placing the card you drew in all the spots you can
    valuesOfIndices = []
    indices = []

    for i in emptyIndices:

        assert -1 == cardsPlaced[i]

        # Put the card you drew in the empty index for this iteration
        newCardsPlaced = [j for j in cardsPlaced]
        newCardsPlaced[i] = card

        # Get the expected value of placing the card in this index
        valuesOfAllNextCards = []
        for nextCard in newCardsLeft:
            valueIfYouPullNextCard = val(nextCard, newCardsLeft, newCardsPlaced)
            valuesOfAllNextCards.append(valueIfYouPullNextCard)

        valuesOfIndices.append(sum(valuesOfAllNextCards)/len(newCardsLeft))
        indices.append(i)

    assert len(valuesOfIndices) <= 4

    bestVal = min(valuesOfIndices)

    memoize[key] = (min(valuesOfIndices), indices[valuesOfIndices.index(bestVal)])

    return min(valuesOfIndices)

cardsPlaced = [-1, -1, -1, -1]
cardsLeft = [0,1,2,3,4,5,6,7,8,9]
cardsDrawn = 0
print(val(cardsDrawn, cardsLeft, cardsPlaced))

print(memoize)