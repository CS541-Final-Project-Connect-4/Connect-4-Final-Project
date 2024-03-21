from random import randint
from connect4_board import is_valid_location, get_next_open_row, drop_piece, score_position, ROW_COUNT, COLUMN_COUNT
#from matplotlib import pyplot

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


def board_to_string(board):
    board_string = ''
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            board_string += str(board[row][col])
    return board_string
    
def greedy_move(board, piece, chosen_column):
   
    if is_valid_location(board, chosen_column):
        row = get_next_open_row(board, chosen_column)
        drop_piece(board, row, chosen_column, piece)
        action_score = score_position(board, piece)
    else:
        action_score = -1
    
    return board, action_score
        
def select_greedy_move(current_state, Q_matrix, all_states, epsilon, board):
   
    chosen_action = None
    
    #epsilon is the probability of a random move.
    probability_dice = randint(0, 100)
    if probability_dice < (epsilon * 100):
        chosen_action = randint(0, 6)
    else:
        if current_state in all_states:
            q_index = all_states[current_state]
            best_score = max(Q_matrix[q_index])
            chosen_action = Q_matrix[q_index].index(best_score)
            while not is_valid_location(board, chosen_action):
               # best_score = 0
                chosen_action = randint(0, 6)
        else:
            chosen_action = randint(0, 6)
            while not is_valid_location(board, chosen_action):
                chosen_action = randint(0, 6)
            #best_score = 0

    #print(f'action chosen: {action}')
    return chosen_action  
 
#current_state = get_current_state(world, robby_row, robby_col)
#print(current_state)

Q_matrix = []
all_states = {}
reward_matrix = []

episodes_N = 5000
steps_M = 42
step_size = 0.2
discount_factor = 0.9
epsilon = 0.5

def Q_table_Player(board, piece, Q_matrix, all_states):
    piece = piece
    epsilon = 0.5 
    #get the current state
    current_state = board_to_string(board)
   # print('Current board to string: ', current_state)
            
    # identify the best next action
    action_index = select_greedy_move(current_state, Q_matrix, all_states, epsilon, board)
    return action_index
    
#display_Q_matrix(Q_matrix, all_states)
Q_Data.close()
State_Data.close()