from connect4_board_minimax import play_game
from connect4_board_minimax import create_board
from connect4_board_minimax import empty_board
import time
import matplotlib.pyplot as plt

new_board = create_board()
num_times = 10


def time_vs_depth(play_game, board):
    list_time = []
    list_iterations = []
    list_won_games = []
    list_depth = [3,4,5,6,7]
    temp = 0
    temp_iterat = 0
    won_game = 0
    temp_won_game = 0
    for depth in list_depth:
        print("Results Depth: ", depth)
        for _ in range(num_times):
            start_time = time.time()
            iteration, won_game = play_game(board, depth)
            temp_iterat += iteration
            temp_won_game += won_game
            end_time = time.time()
            time_result = end_time - start_time
            temp += time_result
            print("Iterations: ", iteration)
            board = empty_board(board)
        #print("end depth", depth)
        temp_aver = temp / num_times
        average_iterate = temp_iterat / num_times
        print("Average time: ", temp_aver)
        print("Average iterations: ", average_iterate)
        
        list_iterations.append(average_iterate)
        list_time.append(temp_aver)
        list_won_games.append(temp_won_game)
        temp_won_game = 0
        temp_iterat = 0 
        temp = 0
        
    #plot 1
    plt.subplot(3,1,1)
    plt.plot(list_depth, list_time, marker='o')
    plt.xlabel('Depth')
    plt.ylabel('Times(seconds)')
    plt.title('Average Time vs Depth')
    plt.grid(True)

    #plot 2
    plt.subplot(3,1,2)
    plt.plot(list_depth, list_won_games, marker='o')
    plt.xlabel('Depth')
    plt.ylabel('Games won')
    plt.title('Games won vs Depth')
    plt.grid(True)


    plt.subplot(3,1,3)
    plt.plot(list_depth,list_iterations, marker='o')
    plt.xlabel('Depth')
    plt.ylabel('No. Iterations')
    plt.grid(True)
    #display plots
    plt.tight_layout()
    plt.show()

time_vs_depth(play_game, new_board)
