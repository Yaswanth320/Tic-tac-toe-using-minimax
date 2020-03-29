

# please run it in anaconda jupyter notebook




from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMAN = -1
ai = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(curstate):

    if wins(curstate, ai):
        score = +1
    elif wins(curstate, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(curstate, player):

    optimalcurstate = [
        [curstate[0][0], curstate[0][1], curstate[0][2]],
        [curstate[1][0], curstate[1][1], curstate[1][2]],
        [curstate[2][0], curstate[2][1], curstate[2][2]],
        [curstate[0][0], curstate[1][0], curstate[2][0]],
        [curstate[0][1], curstate[1][1], curstate[2][1]],
        [curstate[0][2], curstate[1][2], curstate[2][2]],
        [curstate[0][0], curstate[1][1], curstate[2][2]],
        [curstate[2][0], curstate[1][1], curstate[0][2]],
    ]
    if [player, player, player] in optimalcurstate:
        return True
    else:
        return False


def game_over(curstate):

    return wins(curstate, HUMAN) or wins(curstate, ai)


def empty_cells(curstate):

    cells = []

    for x, row in enumerate(curstate):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def moveavl(x, y):

    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def choosenmove(x, y, player):

    if moveavl(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(curstate, depth, player):

    if player == ai:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(curstate):
        score = evaluate(curstate)
        return [-1, -1, score]

    for cell in empty_cells(curstate):
        x, y = cell[0], cell[1]
        curstate[x][y] = player
        score = minimax(curstate, depth - 1, -player)
        curstate[x][y] = 0
        score[0], score[1] = x, y

        if player == ai:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def clean():

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(curstate, computerc, humanc):

    chars = {
        -1: humanc,
        +1: computerc,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in curstate:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(computerc, humanc):

    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'computer turn [{computerc}]')
    render(board, computerc, humanc)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, ai)
        x, y = move[0], move[1]

    choosenmove(x, y, ai)
    time.sleep(1)


def human_turn(computerc, humanc):

    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return


    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{humanc}]')
    render(board, computerc, humanc)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = choosenmove(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():

    clean()
    humanc = ''
    computerc = ''
    first = ''

    while humanc != 'O' and humanc != 'X':
        try:
            print('')
            humanc = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


    if humanc == 'X':
        computerc = 'O'
    else:
        computerc = 'X'


    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice choose another')

    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(computerc, humanc)
            first = ''

        human_turn(computerc, humanc)
        ai_turn(computerc, humanc)

    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{humanc}]')
        render(board, computerc, humanc)
        print('YOU WIN! keep it up')
    elif wins(board, ai):
        clean()
        print(f'computer turn [{computerc}]')
        render(board, computerc, humanc)
        print('YOU LOSE! better luck next time')
    else:
        clean()
        render(board, computerc, humanc)
        print('DRAW! try to improve')

    exit()


if __name__ == '__main__':
    main()
