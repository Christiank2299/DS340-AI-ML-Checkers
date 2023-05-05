# Evaluation function for a given board state
def evaluate(board_state):
    if -2 not in board_state.board:
        # Team 2 has lost
        return 1.0
    elif 2 not in board_state.board:
        # Team 1 has lost
        return 0.0
    else:
        # Neither team has lost yet
        return 0.5

# Minimax algorithm implementation
def minimax(node, depth, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluate(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        #print('BLUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenBlue (node.board):
            child_value = minimax(child, depth-1, False)
            best_value = max(best_value, child_value)
        return best_value
    # If it's the minimizing player's turn
    else:
        #print('RED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        best_value = float('-inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimax(child, depth-1, False)
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
        child_value = minimax(child, depth-1, not maximizing_player)
        if (maximizing_player and child_value > best_value) or (not maximizing_player and child_value < best_value):
            best_move = child
            best_value = child_value
    
    return best_move


# Evaluation function for a given board state
def evaluateABPruning(board_state):
    if -2 not in board_state.board:
        # Team 2 has lost
        return 1.0
    elif 2 not in board_state.board:
        # Team 1 has lost
        return 0.0
    else:
        # Neither team has lost yet
        return 0.5

# Minimax algorithm implementation with alpha-beta pruning
def minimaxABPruning(node, depth, alpha, beta, maximizing_player):
    # Check if we have reached the maximum depth or a terminal state
    if depth == 0 or node.is_terminal(node.board):
        return evaluateABPruning(node)
    
    # If it's the maximizing player's turn
    if maximizing_player:
        best_value = float('-inf')
        for child in node.find_childrenBlue(node.board):
            child_value = minimaxABPruning(child, depth-1, alpha, beta, False)
            best_value = max(best_value, child_value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    # If it's the minimizing player's turn
    else:
        best_value = float('inf')
        for child in node.find_childrenRed(node.board):
            child_value = minimaxABPruning(child, depth-1, alpha, beta, True)
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
        child_value = minimaxABPruning(child, depth-1, alpha, beta, not maximizing_player)
        if child_value > best_value:
            best_move = child
            best_value = child_value
        alpha = max(alpha, best_value)
        if beta <= alpha:
            break
    
    return best_move
