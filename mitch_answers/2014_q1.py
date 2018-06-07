import gurobipy as gb
import random
import math

def get_num_letters(word):
    '''
    Calculates the number of time each letter appears in a word
    and returns it as a list
    '''
    letters = [0] * 26
    for letter in word.lower():
        letters[ord(letter) - 97] += 1
    return letters

def main():
    # Sets
    tiles = 'abcdefghijklmnopqrstuvwxyz'

    # Instantiate model
    model = gb.Model('2014 Question One')

    # Data
    # Word frequencies for each word
    with open('frequencies.txt', 'r') as words_file:
        word_frequencies = [w.strip().split(',') for w in words_file]
    words = [w[0] for w in word_frequencies]
    # Helper convenience functions
    L = range(len(tiles))
    W = range(len(words))
    # Word letters for each word
    word_letters = [get_num_letters(w) for w in words]
    # Word values for each word
    word_values = [int(math.log(int(w[1])) + 1) for w in word_frequencies]
    # N is randomly generated data for letter distributions
    random.seed(3)
    num_tiles = [random.randint(20, 50) for l in L]
    # Number of blank tiles
    num_blanks = 50

    # Variables
    # Whether we've constructed word w
    constructed_words = {w: model.addVar(vtype=gb.GRB.BINARY) for w in W}
    # Number of tiles we need to fulfill all the words for each letter l
    tiles_used = {l: model.addVar(vtype=gb.GRB.INTEGER) for l in L}
    # Number of letters we need to fulfill all the words for each letter l
    letters_used = {l: model.addVar(vtype=gb.GRB.INTEGER) for l in L}

    # Objective
    # Maximise the number of points we get from constructed words
    model.setObjective(gb.quicksum(constructed_words[w] * word_values[w]
                                   for w in W),
                       gb.GRB.MAXIMIZE)

    # Constraints
    # Ensure we are calculating the total number of letters used
    model.addConstrs(gb.quicksum(word_letters[w][l] * constructed_words[w]
                                 for w in W) == letters_used[l] for l in L)
    # Ensure we aren't exceeding the amount of tiles available
    model.addConstrs(tiles_used[l] <= num_tiles[l] for l in L)
    # Ensure we aren't exceeding the amount of blank tiles available
    model.addConstr(gb.quicksum(letters_used[l] - tiles_used[l] for l in L)
                    <= num_blanks)
    # Ensure we aren't exceeding the number of tiles used
    model.addConstrs(letters_used[l] - tiles_used[l] >= 0 for l in L)

    # Solve model
    model.optimize()

    # Print solution
    for w in W:
        if constructed_words[w].x <= 0:
            continue
        print(f'Will construct {words[w]}')
    print(f'Letters used: {[letters_used[l].x for l in L]}')
    print(f'Tiles used: {[tiles_used[l].x for l in L]}')
    print(f'Points achieved: {model.objVal}')

if __name__ == '__main__':
    main()
