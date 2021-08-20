import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYERPIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def is_valid_location(board, col):
    if board[ROW_COUNT - 1][col] == 0:
        return True
    else:
        return False


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    # horizon
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (piece == board[r][c] and piece == board[r][c + 1] and piece == board[r][c + 2] and piece == board[r][
                c + 3]):
                return True

    # vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (piece == board[r][c] and piece == board[r + 1][c] and piece == board[r + 2][c] and piece ==
                    board[r + 3][c]):
                return True

    # positive_diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (piece == board[r][c] and piece == board[r + 1][c + 1] and piece == board[r + 2][c + 2] and piece ==
                    board[r + 3][c + 3]):
                return True

    # negative_diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (piece == board[r][c] and piece == board[r - 1][c + 1] and piece == board[r - 2][c + 2] and piece ==
                    board[r - 3][c + 3]):
                return True


def evaluate_window(window, piece):
    score = 0
    OPPOSITIONPIECE = PLAYERPIECE
    if piece == PLAYERPIECE:
        OPPOSITIONPIECE = AI_PIECE

    if (window.count(piece) == 4):
        score += 10

    elif (window.count(piece) == 3):
        score += 5

    elif (window.count(piece) == 2 or OPPOSITIONPIECE == 2):  ##score계산
        score += 3

    elif (window.count(piece) == 1 or OPPOSITIONPIECE == 3):  ##score계산
        score += 1

    return score


def score_position(board, piece):
    score = 0
    ##center
    center_array = [i for i in board[:][COLUMN_COUNT // 2]]
    score += 10000 * center_array.count(piece)

    ##Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            window = list()
            for i in range(WINDOW_LENGTH):
                window.append(board[r][c + i])
            score += evaluate_window(window, piece)

    ##Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            window = list()
            for i in range(WINDOW_LENGTH):
                window.append(board[r + i][c])
            score += evaluate_window(window, piece)

    ##positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            window = list()
            for i in range(WINDOW_LENGTH):
                window.append(board[r + i][c + i])
            score += evaluate_window(window, piece)

    ##negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            window = list()
            for i in range(WINDOW_LENGTH):
                window.append(board[r - i][c + i])
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    if winning_move(board, AI_PIECE) or winning_move(board, PLAYERPIECE) or len(get_valid_location(board)) == 0:
        return True


def minimax(board, depth, alpha, beta, maximizingPlayer):  ##알파베타
    value = 0
    if (is_terminal_node(board)):
        if winning_move(board, AI_PIECE):
            value = 100000000
            return (None, value)
        elif winning_move(board, PLAYERPIECE):
            value = -10000000
            return (None, value)

        else:
            return (None, 0)

    if depth == 0:
        value = score_position(board, AI_PIECE)
        return (None, value)
    if maximizingPlayer == True:
        value = -10000000
        column = random.choice(get_valid_location(board))
        for col in get_valid_location(board):

            b_copy = board.copy()
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, AI_PIECE)
            none, score = minimax(b_copy, depth - 1, alpha, beta, False)  ##알파베타
            if (score > value):
                value = score
                column = col

            alpha = max(value, alpha)

            if alpha >= beta:  ##알파베타
                break

            print(column)
        return (column, value)

    elif maximizingPlayer == False:
        value = 10000000
        column = random.choice(get_valid_location(board))
        for col in get_valid_location(board):
            b_copy = board.copy()
            row = get_next_open_row(b_copy, col)
            drop_piece(b_copy, row, col, PLAYERPIECE)
            none, score = minimax(b_copy, depth - 1, alpha, beta, True)  ##알파베타
            if (score < value):
                value = score
                column = col

            beta = min(value, beta)

            if alpha >= beta:  ##알파베타
                break

        return (column, value)


def get_valid_location(board):  ##valid column 자리 배열 반환환
    valid_location = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            valid_location.append(c)

    return valid_location


def print_board(board):
    print(board[::-1][:])


"""def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, [c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE])
            pygame.draw.circle(screen, BLACK, [c * SQUARESIZE + SQUARESIZE / 2, (r + 1) * SQUARESIZE + SQUARESIZE / 2],
                               radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   [c * SQUARESIZE + SQUARESIZE / 2, depth - (r * SQUARESIZE + SQUARESIZE / 2)], radius)

            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   [c * SQUARESIZE + SQUARESIZE / 2, depth - (r * SQUARESIZE + SQUARESIZE / 2)], radius)

    ##pygame.display.update()"""

board = create_board()
print_board(board)
game_over = False
first = 0
turn = int(input("누가 먼저?"))
count = 1
##pygame.init()

SQUARESIZE = 70
width = COLUMN_COUNT * SQUARESIZE
depth = (ROW_COUNT + 1) * SQUARESIZE
size = (width, depth)

radius = (SQUARESIZE / 2) - 5

##screen = pygame.display.set_mode(size)
##draw_board(board)
##pygame.display.update()

##myfont = pygame.font.SysFont("monospace", 30)  # 폰트객체 생성

while not game_over:

    if (turn == 0):
        col = int(input("where?"))
        ##if count==1 and col==3:                             ##카운트
        ##    col+=1

        if is_valid_location(board, col):
            r = get_next_open_row(board, col)
            drop_piece(board, r, col, 1)
        elif (is_valid_location(board, col) == False):
            continue
        if (winning_move(board, 1)):
            print("player1 wins!!")
            game_over = True

        count += 1  ##카운트

    elif (turn == 1):
        col = minimax(board, 4, -1000000000, 100000000, True)[0]  ##알파베타
        if count == 1 and col == 3:  ##카운트
            col += 1
        if is_valid_location(board, col):
            r = get_next_open_row(board, col)
            drop_piece(board, r, col, 2)
        elif (is_valid_location(board, col) == False):
            continue
        if (winning_move(board, 2)):
            print("Player 2 wins!!")

            game_over = True
        count += 1  ##카운트

    print_board(board)
    ##draw_board(board)
    turn += 1
    turn = turn % 2




