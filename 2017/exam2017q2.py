cardsPlaced = [-1, -1, -1, -1]
cardsLeft = [0,1,2,3,4,5,6,7,8,9]
cardsDrawn = 0

memoize = {}

def val(cardsDrawn, cardsLeft, cardsPlaced):
    if cardsDrawn == 10:
        tops = int(str(cardsPlaced[0]) + str(cardsPlaced[1]))
        bottoms = int(str(cardsPlaced[2]) + str(cardsPlaced[3]))
        return tops * bottoms

    key = (cardsDrawn, str(cardsLeft), str(cardsPlaced))

    if key in memoize:
        return memoize[key]

    emptyIndices = []
    for i in range(4):
        if cardsPlaced[i] == -1:
            emptyIndices.append(i)

    if len(emptyIndices) == 0:
        tops = int(str(cardsPlaced[0]) + str(cardsPlaced[1]))
        bottoms = int(str(cardsPlaced[2]) + str(cardsPlaced[3]))
        return tops * bottoms

    expectedValueForEachAction = []

    # Work out the values of each of the cards we can draw that are left
    for i in cardsLeft:
        
        # Take the card out
        remainingCards = [card for card in cardsLeft]
        remainingCards.remove(i)

        # Value of all the actions you can take.
        valueOfActions = []

        # Work out the value of placing the card in each slot
        for placeLocation in emptyIndices:
            resultOfPlace = [card for card in cardsPlaced]
            resultOfPlace[placeLocation] = i
            valueOfActions.append(val(cardsDrawn + 1, remainingCards, resultOfPlace))
        expectedValueForEachAction.append(min(valueOfActions))

        # Work out the value of not placing the card, if you have the choice
        if len(emptyIndices) <= len(remainingCards):
            valueOfActions.append(val(cardsDrawn + 1, remainingCards, cardsPlaced))

        # Assume you make the best choice about what to do with the card
        expectedValueForEachAction.append(min(valueOfActions))

    memoize[key] = sum(expectedValueForEachAction)/len(expectedValueForEachAction)

    return sum(expectedValueForEachAction)/len(expectedValueForEachAction)

print(val(0, cardsLeft, cardsPlaced))