from gurobipy import *
import random
import math

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
letterdata = [wordletters(w[0]) for w in words]
# V stores the score of each word, based on a scaled frequency
v = [int(math.log(int(w[1]))+1) for w in words]

W = range(len(letterdata))

random.seed(3)
# N is randomly generated data for letter distributions
N = [random.randint(20,50) for l in L]

# Number of blanks
NBlanks = 50
