import math
from connect4_board import *
from q_table_agent_trained import Q_table_Player
from matplotlib import pyplot
from connect4_board_minimax import minimax

Q_Data = open('Q_matrix.txt', 'r', encoding='UTF-8')
State_Data = open('all_states.txt', 'r', encoding='UTF-8')
Q_matrix = []
all_states = {}
Q_index = 0
for line in Q_Data:
    Q_matrix.append([0,0,0,0,0,0,0])
    for i in range(7):
        value = line.strip('[]\n').split(',')[i]
        value = float(value)
        Q_matrix[Q_index][i] = value
        
    Q_index += 1
    

all_states_index = 0
for line in State_Data:
    current_state = line.strip()
    all_states[current_state] = all_states_index
    all_states_index += 1
#print(all_states)

class RLPlayer():
    
    def get_next_move(self, board, piece):
        return Q_table_Player(board, piece, Q_matrix, all_states)
    
class MinimaxPlayer():
    def get_next_move(self, board, piece, iterate_count):
        depth = 4
        col, minimax_score = minimax(board,depth, -math.inf,math.inf, True, iterate_count)
        return col

#board = create_board()
#print_board(board)
#game_over = False
#turn = 0

# These players can be replaced with the AI players we create, and the random player for training.
Player1 = RLPlayer()
Player2 = MinimaxPlayer()

test_games = 500
game_number = 0
Player1_wins = 0
Player2_wins = 0
win_matrix = []

while game_number < test_games:
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0 
    iterate_count = [0]
    while not game_over:
        
        if turn == 0:
            # Ask for Player 1 input
            col = Player1.get_next_move(board, turn+1)
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print("Player 1 wins!!!")
                    Player1_wins += 1
                    win_matrix.append(1)
                    game_over = True

        else:
            # Ask for Player 2 input
            col = Player2.get_next_move(board, turn+2, iterate_count)
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    print("Player 2 wins!!!")
                    Player2_wins += 1
                    win_matrix.append(2)
                    game_over = True

        print_board(board)
        turn += 1
        turn = turn % 2
    game_number += 1
    
print(f'Player 1 wins: {Player1_wins}, Player 2 wins: {Player2_wins}')
    
x = [x for x in range(len(win_matrix))]
pyplot.plot(x, win_matrix, label = "Winner of each game")
pyplot.title(f'Total Wins for Q-Learning Agent vs Minimax Agent, over sample of 500 games.\nQ-Table Agent wins: {Player1_wins}, Minimax Agent wins: {Player2_wins}')
pyplot.legend()
pyplot.show()
