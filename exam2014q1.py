from gurobipy import *
import random
import math

m = Model("2014 Prac Exam")
m.setParam("MIPGap", 0)

L = range(26)
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Calculates the number of time each letter appears in a word
# and returns it as a list
def wordletters (w):
    letters = [0 for j in L]
    for c in w:
        k = alphabet.index(c)
        if (k >= 0) and (k < 26):
            letters[k] += 1
    return letters

# word frequencies from http://www.wordfrequency.info
# Read in the file and store in in words
# words[w][0] is the word and words[w][1] is the frequency
wordsfile = open('freqs.txt', 'r')
words = [w.strip().split(',') for w in wordsfile]

# Letter data stores the number of times each letter appears in each word
# amountLetterAtIndexXAppearsInWordAtwordsIndex = letterdata[wordsIndex][x]
letterdata = [wordletters(w[0]) for w in words]

# V stores the score of each word, based on a scaled frequency
v = [int(math.log(int(w[1]))+1) for w in words]

W = range(len(letterdata))

random.seed(3)
# N is randomly generated data for letter distributions

# This is how many of each letter we have
N = [random.randint(20,50) for l in L]

# Number of blanks
NBlanks = 50

# We have some number of letters N and 50 blanks, some number of words, each letter has a score,
# Make a set of words with the highest possible score. 

"""
Variables
"""
WordsMade = {}
for i in words:
    WordsMade[i[0]] = m.addVar(vtype=GRB.BINARY)

NumberOfTimesLetterUsed = {}
for i in alphabet:
    NumberOfTimesLetterUsed[i] = m.addVar(vtype=GRB.INTEGER)

NumberOfTilesNeeded = {}
for i in alphabet:
    NumberOfTilesNeeded[i] = m.addVar(vtype=GRB.INTEGER)

"""
Constraints
"""

# Number of letters you need to make all the words you did
# is the number of letters you used
for letterIndex, letter in enumerate(alphabet):
    totalA = 0
    for word in WordsMade:
        totalA += wordletters(word)[letterIndex] * WordsMade[word]
    m.addConstr(totalA == NumberOfTimesLetterUsed[letter])

# Number of tiles you need is at most the number you have
for i in NumberOfTimesLetterUsed:
    m.addConstr(NumberOfTilesNeeded[i] <= N[alphabet.index(i)])

# Only use 50 blanks
blanksUsed = 0
for i in alphabet:
    used = NumberOfTimesLetterUsed[i] - NumberOfTilesNeeded[i]

    # You can't use more tiles than the number of times you needed to use a letter
    m.addConstr(used >= 0)

    blanksUsed += used
m.addConstr(blanksUsed <= 50)

"""
Objective Function
"""
totalScore = 0
for i in NumberOfTimesLetterUsed:
    totalScore += NumberOfTilesNeeded[i] * v[alphabet.index(i)]
m.setObjective(totalScore, GRB.MAXIMIZE)

m.optimize()

for i in alphabet:
    for j in NumberOfTimesLetterUsed:
        if i == j:
            print(i, "letters used", NumberOfTimesLetterUsed[i].x,"tiles used",NumberOfTilesNeeded[i].x , "max", N[alphabet.index(i)])

letterCounts = [0] * len(alphabet)
for i in WordsMade:
    if WordsMade[i].x == 1:
        wordLetterCount = wordletters(i)
        for ind, j in enumerate(wordLetterCount):
            letterCounts[ind] += j

print(letterCounts)
