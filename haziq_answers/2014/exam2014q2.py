
months = [0 ,1 ,2 ,3 ,4 , 5]
demand = [10,20,30,30,20,20]

costOfOneLeftOver = 0.1
maximumStorage = 40
costToOrderAny = 20
costToOrderOne = 2
maximumOrder = 60
sizeOfLots = 10

memoize = {}

def costOfOrder(month, amountLeft, order):
    costOfOrdering = 0
    if order > 0:
        costOfOrdering = costToOrderAny + order * costToOrderOne
    
    howMuchWeHave = amountLeft + order
    amountLeftOver = howMuchWeHave - demand[month]

    assert amountLeftOver >= 0

    costOfLeftOver = 0
    if amountLeftOver > 0:
        costOfLeftOver = costOfOneLeftOver * amountLeftOver

    return costOfOrdering + costOfLeftOver


def transition(month, amountLeft, order):
    amountLeft = max(amountLeft + order - demand[month], 0)
    amountLeft = min(maximumStorage, amountLeft)
    return month + 1, amountLeft

def value(month, amountLeft):
    if month == 6:
        return 0

    if (month, amountLeft) in memoize:
        return memoize[month, amountLeft]["optimalVal"]

    minOrder = max(0, demand[month] - amountLeft)
    actions = range(minOrder, maximumOrder + 10, 10)

    valuesOfActions = []
    for order in actions:

        newStateGivenAction = transition(month, amountLeft, order)
        cost = costOfOrder(month, amountLeft, order)

        valueOfAction = cost + value(newStateGivenAction[0], newStateGivenAction[1])
        valuesOfActions.append(valueOfAction)

    memoize[month, amountLeft] = {"optimalVal": min(valuesOfActions), "optimalAction": actions[valuesOfActions.index(min(valuesOfActions))]}

    return min(valuesOfActions)

print(value(0, 0))

for j in range(7):
    for i in memoize:
        if i[0] == j:
            print(i, memoize[i])