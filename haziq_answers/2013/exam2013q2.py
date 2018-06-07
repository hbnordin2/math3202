totalShots = 10
targetCount = 4
scores = [6, 4, 10, 7]
probabilities = [0.2, 0.4, 0.1, 0.5]

memoize = {}


def immediateReward(shot, previousThrows, action):
    probabilityOfAllMiss = (1-probabilities[action]) ** previousThrows[action]
    probilityWeHitNow = probabilities[action]

    probabilityWeScoreNow = probabilityOfAllMiss * probilityWeHitNow

    score = scores[action]

    return probabilityWeScoreNow * score

def value(shot, previousThrows):

    if shot == 10:
        return 0
    
    key = (shot, str(previousThrows))
    if key in memoize:
        return memoize[key][0]

    actions = range(targetCount)

    valueOfActions = []

    for action in actions:
        valueOfThrow = immediateReward(shot, previousThrows, action)
        new = [i for i in previousThrows]
        new[action] += 1

        totalValue = value(shot+1, new) + valueOfThrow

        valueOfActions.append(totalValue)

    memoize[key] = (max(valueOfActions), actions[valueOfActions.index(max(valueOfActions))])

    return max(valueOfActions)

print(value(0, [0,0,0,0]))