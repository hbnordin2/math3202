import math

seasons = [0,1,2,3,4]
operators = [155, 120, 140, 100, 155]
memoize = {}

def value(season, hiredAlready):
    if season == 5:
        return 0

    key = (season, hiredAlready)
    
    if key in memoize:
        return memoize[key]

    minHires = max(0, operators[season] - hiredAlready)
    maxHires = 155

    hireActions = range(minHires, maxHires + 1)
    fireActions = range(0, max(1, hiredAlready - operators[season] + 1))

    valueOfActions = []
    actions = []

    for hire in hireActions:
        for fire in fireActions:
            costOfHiresAndFires = abs(hire - fire) ** 2 * 200
            
            leftAtTheEnd = hiredAlready + hire - fire

            overShot = leftAtTheEnd - operators[season]

            assert overShot >= 0

            totalCost = costOfHiresAndFires + 2000 * overShot

            valueOfMove = totalCost + value(season + 1, leftAtTheEnd)

            actions.append((hire, fire))
            valueOfActions.append(valueOfMove)

    memoize[key] = min(valueOfActions)
            
    return min(valueOfActions)

print(value(0, 0))