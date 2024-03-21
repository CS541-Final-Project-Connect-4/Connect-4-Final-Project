from platform import node
import numpy as np
import pygame
import sys
import math
import random
import time

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2

WINDOW_LENGTH = 4
Player_AI = 1
Player_RANDOM = 2

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def empty_board(a_board):
    a_board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return a_board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    if  (board[ROW_COUNT-1][col] == 0):
        return True
    return False 


def get_valid_locations(board):
    valid_loc = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            valid_loc.append(col)
    return valid_loc

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_1_PIECE
    if piece == PLAYER_1_PIECE:
        opp_piece = PLAYER_2_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal(board):
    if winning_move(board,1) or winning_move(board,2) or len(get_valid_locations(board))== 0:
        return True 
    else:
        return False

#minimax(node, depth, maximizingplayer)
def minimax(board, depth, alpha, beta, maximizing_player, iterate_count):
    iterate_count[0] += 1
    valid_loc = get_valid_locations(board)

    #depth - 0 or terminal node = game is one or we got the end of the game  
    is_end_node = is_terminal(board)
    if(depth==0) or is_end_node:
        if is_end_node:
            if winning_move(board, Player_AI):
                return None, 1000000000000
            elif winning_move(board, Player_RANDOM):
                return None,-1000000000000
            else:
                return None,0 
        else:
            return (None, score_position(board, Player_AI))
    
    if maximizing_player:
        val = -math.inf
        rand_column = random.choice(valid_loc)
        for col in valid_loc:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, Player_AI)
            temp_score = minimax(board_copy, depth-1, alpha, beta, False, iterate_count)[1]
            if temp_score > val:
                val = temp_score
                rand_column = col
            alpha = max(alpha,val)
            if alpha >= beta:
                break
        return rand_column,val
    else :
        val = math.inf
        rand_column = random.choice(valid_loc)
        for col in valid_loc:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, Player_RANDOM)
            temp_score = minimax(board_copy, depth-1, alpha, beta, True, iterate_count)[1]
            if temp_score < val:
                val = temp_score
                rand_column = col
            beta = min(beta,val)
            if alpha >= beta:
                break
        return rand_column,val

"""
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
"""

class ManualPlayer():
    
    def get_next_move(self, board):
        col = int(input("Player 1 make your selection (0-6):"))
        return col

class RandomPlayer():
    
    def get_next_move(self, board):
        col = np.random.randint(0, COLUMN_COUNT)
        return col

# We can add our AI players here, but I think each AI player should have it's code in a seperate file.
# We can import those files and call the functions in them from these classes.

#class MinimaxPlayer():
    
#class RLPlayer():
    

board = create_board()
print_board(board)
game_over = False
turn = 1

# These players can be replaced with the AI players we create, and the random player for training.
Player1 = ManualPlayer()
Player2 = RandomPlayer()

#starting time
def play_game(board, depth):
    game_over = False
    turn = 1
    iterate_count = [0]
    won_game = 0
    while not game_over:
        if turn == 0:
            # Ask for Player 1 input
            #col = Player1.get_next_move(board)
            col, minimax_score = minimax(board,depth, -math.inf,math.inf, True, iterate_count)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print("Player AI wins!!!", end= ' ')
                    won_game = 1
                    game_over = True
        else:
            # Ask for Player 2 input
            col = Player2.get_next_move(board)
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    print("Player 2 wins!!!", end = ' ')
                    game_over = True

        #print_board(board)
        turn += 1
        turn = turn % 2
    return iterate_count[0], won_game

