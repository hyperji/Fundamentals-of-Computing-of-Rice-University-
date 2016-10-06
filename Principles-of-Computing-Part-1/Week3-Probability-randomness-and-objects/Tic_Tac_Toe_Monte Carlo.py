"""
Monte Carlo Tic-Tac-Toe Player
"""
import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 30        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def found_max_square_list(square_list):
    '''
    found the max value of a square list (a list of lists)
    '''    
    temp = set([])
    max_val = square_list[0][0]
    for dummy_x in square_list:
        for dummy_y in dummy_x:
            temp.add(dummy_y)
            if max_val < dummy_y:
                max_val = dummy_y
    temp.remove(max_val)
    return max_val, list(temp)

def move_player(board, player):
    '''
    move the player randomly across the empty squares
    '''    
    empty_squares = board.get_empty_squares()
    target_move = random.choice(empty_squares)
    board.move(target_move[0], target_move[1], player)

    
def mc_trial(board, player):
    '''
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by making random moves,
    alternating between players. The function should return when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything. In other words, 
    the function should modify the board input.
    '''
    while True:
        # move player1
        move_player(board, player)
        if board.check_win() != None:
            break
        # move player2
        move_player(board, provided.switch_player(player))
        if board.check_win() != None:
            break
   
        
def mc_update_scores(scores, board, player):
    '''
     This function takes a grid of scores (a list of lists) with the same dimensions
     as the Tic-Tac-Toe board, 
     a board from a completed game, and which player the machine player is. 
     The function should score the completed board and update the scores grid.
     As the function updates the scores grid directly, it does not return anything,
    '''
    #print scores
    dim = board.get_dim()
    if board.check_win() == player:
        for dummy_x in range(dim):
            for dummy_y in range(dim):
                if board.square(dummy_x, dummy_y) == player:
                    scores[dummy_x][dummy_y] += SCORE_CURRENT
                elif board.square(dummy_x, dummy_y) == provided.EMPTY:
                    scores[dummy_x][dummy_y] += 0
                elif board.square(dummy_x, dummy_y) == provided.switch_player(player):
                    scores[dummy_x][dummy_y] -= SCORE_OTHER
    
    elif board.check_win() == provided.switch_player(player):
        for dummy_x in range(dim):
            for dummy_y in range(dim):
                if board.square(dummy_x, dummy_y) == player:
                    scores[dummy_x][dummy_y] -= SCORE_CURRENT
                elif board.square(dummy_x, dummy_y) == provided.EMPTY:
                    scores[dummy_x][dummy_y] += 0
                elif board.square(dummy_x, dummy_y) == provided.switch_player(player):
                    scores[dummy_x][dummy_y] += SCORE_OTHER


    

def get_best_move(board, scores):
    '''
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple. 
    It is an error to call this function with a board that has no empty squares 
    (there is no possible next move), 
    so your function may do whatever it wants in that case. 
    The case where the board is full will not be tested.
    '''
    #print board.get_empty_squares()
    dim = board.get_dim()
    if board.get_empty_squares() == []:
        pass
    else:
        finished = False
        max_score, temp = found_max_square_list(scores)
        while not finished:
            empty_squares = board.get_empty_squares()
            #print empty_squares
            candidate_squares = []
            for dummy_x in range(dim):
                for dummy_y in range(dim):
                    if max_score == scores[dummy_x][dummy_y] and (dummy_x, dummy_y) in empty_squares:
                        candidate_squares.append((dummy_x, dummy_y))
            #print candidate_squares
            if candidate_squares != []:
                best_move = random.choice(candidate_squares)
                return best_move
            if temp == []:
                finished = True
            else:
                max_score = max(temp)
                temp.remove(max(temp))               
        best_move = random.choice(candidate_squares)
        return best_move
  

def mc_move(board, player, trials):
    '''
     This function takes a current board, which player the machine player is, 
     and the number of trials to run. 
     The function should use the Monte Carlo simulation described above to
     return a move for the machine player in the form of a (row, column) tuple.
     Be sure to use the other functions you have written!
    '''
    dim = board.get_dim()
    scores = [[0]*dim for dummy in range(dim)]
    trial_counter = 0
    while trial_counter < trials:
        test_board = board.clone()
        mc_trial(test_board, player)
        mc_update_scores(scores, test_board, player)
        trial_counter += 1
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
