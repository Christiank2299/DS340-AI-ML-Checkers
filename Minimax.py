# Evaluation function for a given board state
import copy 


def minimax(node, depth, maximizing_player):
    if depth == 0 or node.is_terminal(node.board ):
        return node.evaluate(), node
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for child in node.find_childrenRed(node.board):
            child_eval = minimax(child, depth - 1, False)[0]
            if child_eval > max_eval:
                max_eval = child_eval
                best_move = child
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for child in node.find_childrenBlue(node.board):
            child_eval = minimax(child, depth - 1, True)[0]
            if child_eval < min_eval:
                min_eval = child_eval
                best_move = child
        return min_eval, best_move
    

def minimax_ab(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.is_terminal(node.board):
        return node.evaluate(), node
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for child in node.find_childrenRed(node.board):
            child_eval = minimax_ab(child, depth - 1, alpha, beta, False)[0]
            if child_eval > max_eval:
                max_eval = child_eval
                best_move = child
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for child in node.find_childrenBlue(node.board):
            child_eval = minimax_ab(child, depth - 1, alpha, beta, True)[0]
            if child_eval < min_eval:
                min_eval = child_eval
                best_move = child
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move



#def evaluate2(board_state):
#    if -2 not in board_state.board:
        # Team 2 has lost
#        return 1.0
#    elif 2 not in board_state.board:
        # Team 1 has lost
#        return 0.0
#    else:
        # Neither team has lost yet
#        return 0.5
    
def evaluate(board_state):
    # Calculate the total piece count for each player
    red_count = board_state.board.count(-1) + board_state.board.count(-2)
    blue_count = board_state.board.count(1) + board_state.board.count(2)
    
    # Calculate the total king count for each player
    red_king_count = board_state.board.count(-2)
    blue_king_count = board_state.board.count(2)
    
    # Calculate the total piece position score for each player
    red_position_score = 0
    blue_position_score = 0
    for i in range(len(board_state.board)):
        if board_state.board[i] == -1:
            red_position_score += i // 4  # add row number
        elif board_state.board[i] == -2:
            red_position_score += 1.5 * (i // 4)  # add row number, weighted by 1.5 for kings
        elif board_state.board[i] == 1:
            blue_position_score += (7 - i // 4)  # add inverse row number
        elif board_state.board[i] == 2:
            blue_position_score += 1.5 * (7 - i // 4)  # add inverse row number, weighted by 1.5 for kings
            
    # Calculate the overall score as a weighted sum of the different factors
    red_score = (2*red_count + red_king_count + 0.5*red_position_score) / (2*red_count + 2*red_king_count + 14*4)
    blue_score = (2*blue_count + blue_king_count + 0.5*blue_position_score) / (2*blue_count + 2*blue_king_count + 14*4)
    return blue_score - red_score  # return the difference between the blue score and red score


# Minimax algorithm implementation
def minimax2(node, depth, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluate(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        #print('BLUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenBlue (node.board):
            child_value = minimax2(child, depth-1, False)
            best_value = max(best_value, child_value)
        return best_value
    # If it's the minimizing player's turn
    else:
        #print('RED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimax2(child, depth-1, False)
            best_value = max(best_value, child_value)
        return best_value
    

def minimax2Blue(node, depth, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluate(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        #print('BLUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimax2Blue(child, depth-1, False)
            best_value = max(best_value, child_value)
        return best_value
    # If it's the minimizing player's turn
    else:
        #print('RED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenBlue(node.board):
            child_value = minimax2Blue(child, depth-1, False)
            best_value = max(best_value, child_value)
        return best_value
    

# Function to get the best move for a given board state using the minimax algorithm
def get_best_move(board_state, depth):
    # Check which player's turn it is
    #if board_state.team == 1:
    #    print('BLUE BEST MOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #    children = board_state.find_childrenBlue(board_state.board)
    #    maximizing_player = True
    #else:
    print('RED BEST MOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    children = board_state.find_childrenRed(board_state.board)
    maximizing_player = False
    
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    
    # Try each possible move and get the one with the best value
    for child in children:
        child_value = minimax2(child, depth-1, not maximizing_player)
        if (maximizing_player and child_value > best_value) or (not maximizing_player and child_value < best_value):
            best_move = child
            best_value = child_value
    
    return best_move

def get_best_moveBlue(board_state, depth):
    # Check which player's turn it is
    #if board_state.team == 1:
    #    print('BLUE BEST MOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #    children = board_state.find_childrenBlue(board_state.board)
    #    maximizing_player = True
    #else:
    print('RED BEST MOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    children = board_state.find_childrenBlue(board_state.board)
    maximizing_player = False
    
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    
    # Try each possible move and get the one with the best value
    for child in children:
        child_value = minimax2Blue(child, depth-1, not maximizing_player)
        if (maximizing_player and child_value > best_value) or (not maximizing_player and child_value < best_value):
            best_move = child
            best_value = child_value
    
    return best_move


# Evaluation function for a given board state
#def evaluateABPruning2(board_state):
#    if -2 not in board_state.board:
        # Team 2 has lost
#        return 1.0
#    elif 2 not in board_state.board:
        # Team 1 has lost
 #       return 0.0
 #   else:
        # Neither team has lost yet
 #       return 0.5
    
def evaluateABPruning(board_state):
    # Calculate the total piece count for each player
    red_count = board_state.board.count(-1) + board_state.board.count(-2)
    blue_count = board_state.board.count(1) + board_state.board.count(2)
    
    # Calculate the total king count for each player
    red_king_count = board_state.board.count(-2)
    blue_king_count = board_state.board.count(2)
    
    # Calculate the total piece position score for each player
    red_position_score = 0
    blue_position_score = 0
    for i in range(len(board_state.board)):
        if board_state.board[i] == -1:
            red_position_score += i // 4  # add row number
        elif board_state.board[i] == -2:
            red_position_score += 1.5 * (i // 4)  # add row number, weighted by 1.5 for kings
        elif board_state.board[i] == 1:
            blue_position_score += (7 - i // 4)  # add inverse row number
        elif board_state.board[i] == 2:
            blue_position_score += 1.5 * (7 - i // 4)  # add inverse row number, weighted by 1.5 for kings
            
    # Calculate the overall score as a weighted sum of the different factors
    red_score = (2*red_count + red_king_count + 0.5*red_position_score) / (2*red_count + 2*red_king_count + 14*4)
    blue_score = (2*blue_count + blue_king_count + 0.5*blue_position_score) / (2*blue_count + 2*blue_king_count + 14*4)
    return blue_score - red_score  # return the difference between the blue score and red score


# Minimax algorithm implementation with alpha-beta pruning
def minimax2ABPruning(node, depth, alpha, beta, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluateABPruning(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        best_value = float('-inf')
        for child in node.find_childrenBlue(node.board):
            child_value = minimax2ABPruning(child, depth-1, alpha, beta, False)
            best_value = max(best_value, child_value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    # If it's the minimizing player's turn
    else:
        best_value = float('inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimax2ABPruning(child, depth-1, alpha, beta, True)
            best_value = min(best_value, child_value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value
    



def minimax2ABPruningBlue(node, depth, alpha, beta, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluateABPruning(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        best_value = float('-inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimax2ABPruning(child, depth-1, alpha, beta, False)
            best_value = max(best_value, child_value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    # If it's the minimizing player's turn
    else:
        best_value = float('inf')
        for child in node.find_childrenBlue(node.board):
            child_value = minimax2ABPruning(child, depth-1, alpha, beta, True)
            best_value = min(best_value, child_value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value
    
    

# Function to get the best move for a given board state using the minimax algorithm with alpha-beta pruning
def get_best_moveABPruning(board_state, depth):
    children = board_state.find_childrenRed(board_state.board)
    maximizing_player = False
    
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    # Try each possible move and get the one with the best value
    for child in children:
        child_value = minimax2ABPruning(child, depth-1, alpha, beta, not maximizing_player)
        if child_value > best_value:
            best_move = child
            best_value = child_value
        alpha = max(alpha, best_value)
        if beta <= alpha:
            break
    
    return best_move

def get_best_moveABPruningBlue(board_state, depth):
    children = board_state.find_childrenBlue(board_state.board)
    maximizing_player = False
    
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    # Try each possible move and get the one with the best value
    for child in children:
        child_value = minimax2ABPruningBlue(child, depth-1, alpha, beta, not maximizing_player)
        if child_value > best_value:
            best_move = child
            best_value = child_value
        alpha = max(alpha, best_value)
        if beta <= alpha:
            break
    
    return best_move


