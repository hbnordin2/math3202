"""
Given a string containing just the characters '(' and ')', 
find the length of the longest valid (well-formed) parentheses substring.
"""

"""
What is the best one that includes the middle index?
What is the best one that includes the left-most index?
What is the best one that includes the right-most index?
"""

memoize = {}

def isValid(parathesis):

    stack = []
    for i in parathesis:
        if i == ")" and stack[-1] == "(":
            stack = stack[:-1]
    
    if len(stack != 0):
        return False

def value(parathesis):
    if parathesis == "":
        return 0
    
    key = parathesis
    if key in memoize:
        return memoize[key]

    actions = []

    for i in range(len(parathesis)):
        actions.append(i)

    """
    Find best one on the left, best one on the right, best one including index
    """

    for i in actions:
        left, right = i
        
    
