from random import randint
from connect4_board import *
from matplotlib import pyplot



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
        best_score = Q_matrix[all_states[current_state]][chosen_action]
    else:
        q_index = all_states[current_state]
        best_score = max(Q_matrix[q_index])
        chosen_action = Q_matrix[q_index].index(best_score)
        while not is_valid_location(board, chosen_action):
                best_score = 0
                chosen_action = randint(0, 6)

    #print(f'action chosen: {action}')
    return best_score, chosen_action  
    

def generate_Q_matrix(all_states, current_state, Q_matrix):
    if current_state not in all_states:
        all_states[current_state] = len(all_states)
        Q_matrix.append([0, 0, 0, 0, 0, 0, 0])
        return True
    else:
        return False
def get_current_Q_value(Q_matrix, all_states, current_state, action_index):
    q_index = all_states[current_state]
    return Q_matrix[q_index][action_index]

def get_max_Q_value(Q_matrix, all_states, current_state):
    if max(Q_matrix[all_states[current_state]]) == 0:
        if Q_matrix[all_states[current_state]][0] == 'C':
            return 10
        else:
            return 0
    else:
        return max(Q_matrix[all_states[current_state]])

def update_Q_matrix(Q_matrix, all_states, current_state, action_index, updated_Q):
    Q_matrix[all_states[current_state]][action_index] = updated_Q
    return Q_matrix 

def display_Q_matrix(Q_matrix, all_states):
    for i in range(len(Q_matrix)):
        print(f'Q-values at index{i}: {Q_matrix[i]}')
 
#current_state = get_current_state(world, robby_row, robby_col)
#print(current_state)

Q_matrix = []
all_states = {}
win_matrix = []
total_wins = 0

episodes_N = 5000
steps_M = 42
step_size = 0.2
discount_factor = 0.9
epsilon = 0.5

Player2 = RandomPlayer()

while episodes_N > 0:
    board = create_board()
    print_board(board)
    print('Episode:', (50 - episodes_N))
    game_over = False
    turn = 0
    total_reward = 0
    
    while steps_M > 0 and not game_over:
        
        if turn == 0:
            piece = 1    
            #get the current state
            current_state = board_to_string(board)
            generate_Q_matrix(all_states, current_state, Q_matrix)
            
            # identify the best next action
            maxA, action_index = select_greedy_move(current_state, Q_matrix, all_states, epsilon, board)
            new_board, reward = greedy_move(board, piece, action_index)
            max_state = board_to_string(new_board)
            generate_Q_matrix(all_states, max_state, Q_matrix)
            
            
            
            current_Q = get_current_Q_value(Q_matrix, all_states, current_state, action_index)
            max_Q = get_max_Q_value(Q_matrix, all_states, max_state)
            
            updated_Q = current_Q + (step_size * (reward + (discount_factor * max_Q) - current_Q))
                
            Q_matrix = update_Q_matrix(Q_matrix, all_states, current_state, action_index, updated_Q)
            
            #world.display_grid_world()
            print((200 - steps_M), 'reward:', reward, 'Total reward:', total_reward, 'Current state:', current_state, 'Action:', action_index, 'current Q', current_Q, 'Max Q:', max_Q, 'Updated Q:', updated_Q)
            #display_Q_matrix(Q_matrix, all_states)
            #print(f'All states: {all_states}, \n Reward matrix: {reward_matrix}') 
            total_reward += reward
            if winning_move(board, 1):
                print("Player 1 wins!!!")
                total_wins += 1
                game_over = True
            
            
        else:
            # Ask for Player 2 input
            col = Player2.get_next_move(board)
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    print("Player 2 wins!!!")
                    game_over = True
        turn += 1
        turn = turn % 2
        steps_M -= 1
    
    win_matrix.append(total_wins)
    steps_M = 42
    episodes_N -= 1
    if episodes_N % 50 == 0:
        epsilon -= 0.001
    

#display_Q_matrix(Q_matrix, all_states)

with open('Q_matrix.txt', 'w') as f:
    for i in range(len(Q_matrix)):
        f.write(f'{Q_matrix[i]}\n')
#print(f'All states: {all_states}, \n Reward matrix: {win_matrix}')

with open('all_states.txt', 'w') as g:
    for i in all_states:
        g.write(f'{i}\n')

g.close()
f.close()

x = [x for x in range(len(win_matrix))]
pyplot.plot(x, win_matrix, label = "Total Number of Wins")
pyplot.title('Total Wins for Q-Learning Agent')
pyplot.legend()
pyplot.show()