from random import *
from puzzle import GameGrid

def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0],
                  accumulate(fn, initial, seq[1:]))

def flatten(mat):
    return [num for row in mat for num in row]

def new_game_matrix(n):
    toRet = [[0 for i in range(n)] for j in range(n)]
    return toRet

def has_zero(mat):
    flattened = flatten(mat)
    return (0 in flattened)

def add_two(mat):
    if not has_zero(mat):
        return mat
    else:
        done = False
        while not done:
            row = randint(0, len(mat) - 1)
            column = randint(0, len(mat[0]) - 1)
            if mat[row][column] == 0:
                mat[row][column] = 2
                done = True
        return mat

def game_status(mat):
    # win: player has created a tile with the value 2048
    if 2048 in mat:
        return 'win'

    # lose: there are no possible moves and no empty tiles on the board
    if not has_zero(mat): # no empty tiles
        # check horizontal
        lost = True
        for row in mat:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    lost = False
        # check vertical
        for i in range(len(mat[0])):
            for j in range(len(mat) - 1):
                if mat[j][i] == mat[j + 1][i]:
                    lost = False
        if lost == True:
            return 'lose'

    return 'not over'

def transpose(mat):
    n = len(mat)
    m = len(mat[0])
    # swap row length and column length
    new_matrix = [[0 for i in range(n)] for j in range(m)]
    for j in range(m):
        for i in range(n):
            new_matrix[j][i] = mat[i][j]
    return new_matrix

'''
def transpose(mat):
    result = []
    for i in range(len(mat[0])):
        result += [list(map(lambda x: x[i], mat))]
    return result
'''

def reverse(mat):
    toRet = []
    for row in mat:
        toRet.append(row[::-1])

    return toRet

def merge_left(mat):
    new_mat = new_game_matrix(len(mat))
    score_increment = 0
    for i in range(len(mat)):
        no_zeroes = list(filter(lambda x: x!= 0, mat[i]))
        new_row = []
        while no_zeroes:
            if len(no_zeroes) >= 2:
                if no_zeroes[0] == no_zeroes[1]:
                    # merge same number and append
                    new_row.append((no_zeroes[0])*2)
                    score_increment += no_zeroes[0] * 2
                    no_zeroes.pop(1)
                else:
                    # append number without merging
                    new_row.append(no_zeroes[0])
                no_zeroes.pop(0)
            else:
                new_row.append(no_zeroes[0])
                no_zeroes.pop(0)

        # fill up remaining spaces
        while len(new_row) < len(mat[0]):
            new_row.append(0)
        new_mat[i] = new_row

    is_valid = new_mat != mat
    return (new_mat, is_valid, score_increment)

def merge_right(mat):
    return reverse(merge_left(reverse(mat))[0]), merge_left(reverse(mat))[1], merge_left(reverse(mat))[2]

def merge_up(mat):
    return (transpose(merge_left(transpose(mat))[0]), merge_left(transpose(mat))[1], merge_left(transpose(mat))[2])

def merge_down(mat):
    return (transpose(merge_right(transpose(mat))[0]), merge_right(transpose(mat))[1], merge_right(transpose(mat))[2])

def text_play():
    def print_game(mat, score):
        for row in mat:
            print(''.join(map(lambda x: str(x).rjust(5), row)))
        print('score: ' + str(score))
    GRID_SIZE = 4
    score = 0
    mat = add_two(add_two(new_game_matrix(GRID_SIZE)))
    print_game(mat, score)
    while True:
        move = input('Enter W, A, S, D or Q: ')
        move = move.lower()
        if move not in ('w', 'a', 's', 'd', 'q'):
            print('Invalid input!')
            continue
        if move == 'q':
            print('Quitting game.')
            return
        move_funct = {'w': merge_up,
                      'a': merge_left,
                      's': merge_down,
                      'd': merge_right}[move]
        mat, valid, score_increment = move_funct(mat)
        if not valid:
            print('Move invalid!')
            continue
        score += score_increment
        mat = add_two(mat)
        print_game(mat, score)
        status = game_status(mat)
        if status == "win":
            print("Congratulations! You've won!")
            return
        elif status == "lose":
            print("Game over. Try again!")
            return

def make_state(matrix, total_score):
    return (matrix, total_score)

def get_matrix(state):
    return state[0]

def get_score(state):
    return state[1]

def make_new_game(n):
    toRet = new_game_matrix(n)
    add_two(add_two(toRet))
    return (toRet, 0)

def left(state):
    info = merge_left(state[0])
    new_mat = add_two(info[0])
    valid = info[1]
    new_score = state[1] + info[2]
    new_state = make_state(new_mat, new_score)
    return(new_state, valid)


def right(state):
    info = merge_right(state[0])
    new_mat = add_two(info[0])
    valid = info[1]
    new_score = state[1] + info[2]
    new_state = make_state(new_mat, new_score)
    return (new_state, valid)

def up(state):
    info = merge_up(state[0])
    new_mat = add_two(info[0])
    valid = info[1]
    new_score = state[1] + info[2]
    new_state = make_state(new_mat, new_score)
    return (new_state, valid)

def down(state):
    info = merge_down(state[0])
    new_mat = add_two(info[0])
    valid = info[1]
    new_score = state[1] + info[2]
    new_state = make_state(new_mat, new_score)
    return (new_state, valid)


# Do not edit this #
game_logic = {
    'make_new_game': make_new_game,
    'game_status': game_status,
    'get_score': get_score,
    'get_matrix': get_matrix,
    'up': up,
    'down': down,
    'left': left,
    'right': right,
    'undo': lambda state: (state, False)
}

# UNCOMMENT THE FOLLOWING LINE TO START THE GAME (WITHOUT UNDO)
gamegrid = GameGrid(game_logic)
