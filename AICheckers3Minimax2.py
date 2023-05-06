


#HyperParameters
numrollout = 10    #Number of rollouts performed
sqlUpdate_after_NGames = 5  #The sql speed database updates after these many games

#Set up
import sqlite3 as sql 
import pygame
import random as rand
import copy
from Testing_MCTS import MCTS
import SQLManipulator as sqlm
from Minimax import get_best_move, get_best_moveBlue, get_best_moveABPruning, get_best_moveABPruningBlue, minimax, minimax_ab

#Colors
black = (0,0,0)
grey = (120,120,120)
white = (0,100, 0)
red = (255,0,0)
lightred = (255,120,120)
darkred = (128,0,0)
green = (0,255,0)
lightgreen = (120,200,120)
darkgreen = (0,128,0)
blue = (0,0,255)
lightblue = (120,120,255)
darkblue = (0,0,128)

#Variable Declaration
board = []
direc = {'upr':-7,'upl':-9,'dl':7,'dr':9}
options1 = [] #Moves team 1 can do
options2 = [] #Moves team 2 can do
avgRlist = [] #Maps the highest reward per state
winlist = [] #Keeps track of each win
pclock = pygame.time.Clock() #Keeps track of the total running time
simclock = pygame.time.Clock() #Keeps track of the time simulating games
BADGAME = pygame.USEREVENT + 1 #Pygame event for timer of games
totaltime = 0
square = None #Used in UserMove

       
#Class Board_state is an instance of the board that's hashable and can be ran through MCTS
class Board_State():
    def __init__(self, board):
        self.board = board
        self.options1, self.options2 = CanMove(self.board)
        self.options = self.options1 + self.options2
        self.team = 1

        self.blue_pieces = 0
        self.red_pieces = 0
        self.blue_kings = 0
        self.red_kings = 0

        for i in range(len(self.board)):
            if self.board[i] == 1:
                self.blue_pieces += 1
            elif self.board[i] == -1:
                self.red_pieces += 1
            elif self.board[i] == 2:
                self.blue_kings += 1
            elif self.board[i] == -2:
                self.red_kings += 1
    
    def count_blue_pieces(self):
        return self.blue_pieces

    def count_red_pieces(self):
        return self.red_pieces

    def count_blue_kings(self):
        return self.blue_kings

    def count_red_kings(self):
        return self.red_kings



#The find_children() method takes a board parameter and returns a set of possible board states resulting from legal moves 
# that the current player can make.
    def find_childrenBlue(self, board):
        children = set()
        #Update the options
        self.options1, self.options2 = CanMove(board)
        for option in self.options1:
            board_copy = copy.deepcopy(board)
            move(board_copy, option[0], option[1], option[2], option[3])
            children.add(Board_State(board_copy))
        return children
    
    def find_childrenRed(self, board):
        children = set()
        #Update the options
        self.options1, self.options2 = CanMove(board)
        for option in self.options2:
            board_copy = copy.deepcopy(board)
            move(board_copy, option[0], option[1], option[2], option[3])
            children.add(Board_State(board_copy))
        return children


#The find_oppchildren() method is similar to find_children(), but instead finds possible board states that the opposing player can make.
    def find_oppchildrenBlue(self,board):
        children = set()
        self.options1, self.options2 = CanMove(board)
        for option in self.options2:
            board_copy = copy.deepcopy(board)
            move(board_copy, option[0], option[1], option[2], option[3])
            children.add(Board_State(board_copy))
        return children

    
#The find_oppchildren() method is similar to find_children(), but instead finds possible board states that the opposing player can make.
    def find_oppchildrenRed(self,board):
        children = set()
        self.options1, self.options2 = CanMove(board)
        for option in self.options1:
            board_copy = copy.deepcopy(board)
            move(board_copy, option[0], option[1], option[2], option[3])
            children.add(Board_State(board_copy))
        return children

# The find_random_child() method chooses a random legal move for the current player and returns the resulting board state. 
# If the resulting board state is not a terminal state, it chooses a random legal move for the opposing player 
# and returns the resulting board state.
    def find_random_childBlue(self, board):
        board_copy = copy.deepcopy(board)
        
        self.options1, self.options2 = CanMove(board)
        choice = rand.choice(self.options1)
        move(board_copy, choice[0], choice[1], choice[2], choice[3])

        if not self.is_terminal(board_copy):
            self.options1, self.options2 = CanMove(board_copy)
            choice2 = rand.choice(self.options2)        
            move(board_copy, choice2[0], choice2[1], choice2[2], choice2[3])

        return Board_State(board_copy)
    
    def find_random_childRed(self, board):
        board_copy = copy.deepcopy(board)
        
        self.options1, self.options2 = CanMove(board)
        choice = rand.choice(self.options2)
        move(board_copy, choice[0], choice[1], choice[2], choice[3])

        if not self.is_terminal(board_copy):
            self.options1, self.options2 = CanMove(board_copy)
            choice2 = rand.choice(self.options1)        
            move(board_copy, choice2[0], choice2[1], choice2[2], choice2[3])

        return Board_State(board_copy)

# The is_terminal() method checks if the current board state is a terminal state, meaning either one of the players has no more legal moves. 
# If the current state is a terminal state, the method returns True, otherwise it returns False.
    def is_terminal(self, board):
        self.options1,self.options2 = CanMove(board)
        if len(options1) == 0 or len(options2) == 0:
            return True
        else:
            return False

# The reward() method determines the reward for a given board state. If the current player has all their pieces removed from the board, 
# they lose and the method returns 0. If the opposing player has all their pieces removed from the board, the current player wins 
# and the method returns 1. Otherwise, if neither player has lost, the method returns a reward of 0.5, indicating a tie or a draw.
    def reward(self,board):
        if (-2 in board or -1 in board) and not (2 in board or 1 in board):
            return 0
        elif (2 in board or 1 in board) and not (-2 in board or -1 in board):
            return 1
        else:
            #Tie instances shouldn't really be a thing
            #Someone is winning
            #print("Tie Instance")
            return .5
    


    def evaluate(self):
        return (self.count_blue_pieces() - self.count_red_pieces())+ (self.count_blue_kings() * 0.5 - self.count_red_kings() * 0.5)

class Game():
    #__init__(self, size) - Initializes the Game() object with a specified screen size and sets the running attribute to True.
    def __init__(self,size):
        self.screen = pygame.display.set_mode((size,size))
        self.size = size / 8
        self.running = True

    #Init makes the background
    #init(self) - Initializes the background of the game screen and creates the checkered board. 
    # Calls PieceUpdate() to update the pieces on the board and CanMove() to check for valid moves.
    def init(self):
        self.screen.fill(grey)
        #BADGAME is just a game taking longer than 1000 milliseconds
        #pygame.time.set_timer(BADGAME, 60000) #This won't run visual slow games
        MakeBoard()

        #Makes the background board checkered
        for index in range(len(board)):
            if board[index] == 'null':
                pygame.draw.rect(self.screen, white, ((index % 8) * self.size, (index // 8) * self.size, self.size, self.size ))
        UpdateScreen()
        self.PieceUpdate()
        CanMove(board)

    
    #PieceUpdate(self) - Updates the visuals of the pieces on the board based on the state of the board list.
    def PieceUpdate(self):
        for index in range(len(board)):
            if board[index] == 1:
                pygame.draw.circle(self.screen,  lightblue, (int((index % 8) * self.size + self.size / 2), int((index // 8) * self.size + self.size / 2)), int(self.size / 2 - 5))
            elif board[index] == -1:
                pygame.draw.circle(self.screen,  lightred, (int((index % 8) * self.size + self.size / 2), int((index // 8) * self.size + self.size / 2)), int(self.size / 2 - 5))
            elif board[index] == 2:
                pygame.draw.circle(self.screen,  darkblue, (int((index % 8) * self.size + self.size / 2), int((index // 8) * self.size + self.size / 2)), int(self.size / 2 - 5))
            elif board[index] == -2:
                pygame.draw.circle(self.screen,  darkred, (int((index % 8) * self.size + self.size / 2), int((index // 8) * self.size + self.size / 2)), int(self.size / 2 - 5))
            elif board[index] == 0:
                pygame.draw.rect(self.screen, grey, ((index % 8) * self.size, (index // 8) * self.size, self.size, self.size ))
            else:
                continue

    #gameEvent is the pygame event handler.. Checks for BADGAME and QUIT
    #gameEvent(self) - Handles user input and quits the game when necessary. Specifically, it listens for pygame.QUIT 
    #and pygame.KEYDOWN events. If pygame.QUIT is detected, the game is ended and self.running is set to False. 
    # If pygame.KEYDOWN is detected and the user presses the escape key, the game is ended and self.running is set to False.
    def gameEvent(self):
        if pygame.event.get(pygame.QUIT): 
            #This updates at the beginning of the loop so it runs an extra time
            print("\nEnding\n")
            self.running = False
        for event in pygame.event.get():
            if event.type == BADGAME:
                print("BADGAME event handled\n")
                self.Restart()    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("\nEnding\n")
                    self.running = False

    #Restart(self) - Restarts the game by resetting the board, winlist, and avgRlist attributes to their initial state. 
    # It also writes avgRlist to a file if the game ended in a win. Calls init() to initialize the board again.
    def Restart(self):
        global board, winlist, avgRlist

        tietest = []

        for index in range(len(board)):
            if board[index] == 1 or board[index] == 2:
                tietest.append(1)
            if board[index] == -1 or board[index] == -2:
                tietest.append(-1)

        
        txtfile = open("MoveSets.txt", 'a')
        if 1 in tietest and not(1 in tietest and -1 in tietest):
            winlist.append(1)
            txtfile.write(str(avgRlist) + "\n")
        if -1 in tietest and not(1 in tietest and -1 in tietest):
            winlist.append(-1)
            txtfile.write(str(avgRlist) + "\n")
        txtfile.close()
        
        #if 1 in tietest and -1 in tietest:     #Tie logic: if the board has 1 and -1 then it's a tie
            #print("Tie")


        if len(winlist) % 1 == 0: #This throws error if it doesn't get to complete the first game lul
            PrintStats()
        
        avgRlist = []
        board = []
        self.init()


#Methods
#UpdateScreen = pygame.display.update()
def UpdateScreen():
    pygame.display.update()

#move is the checkers movement. Doesn't use logic, can't allow user rn
#move: Represents a move in the checkers game. 
# It takes five parameters - board (the board state), index (the index of the piece being moved), dire (the direction of the move), 
# status (the status of the moving piece), and newstat (the status of the destination square). 
# Depending on the value of newstat, the method performs either a simple move or a capture move. 
# After the move is made, the method calls CanMove to check for any additional moves.
def move(board,index,dire,status,newstat):
    if newstat == 0:
        board[index] = 0
        board[index + dire] = status
    else:
        board[index] = 0
        board[index + dire] = 0
        board[index + dire * 2] = status

    CanMove(board)

#CompMove = randomly chooses move in options, uses move func
#CompMove: Represents a move by the computer player. It takes a parameter team (the team for which the computer is playing). 
#Depending on the value of team, it randomly chooses a move from either options1 or options2 and calls the move method to make the move.
def CompMove(team):
    if team == 1:
        #choose = self.ScoreNodes(board,options1)
        choose = rand.choice(options1)
    elif team == -1:
        #choose = self.ScoreNodes(board,options2)
        #choose = sm.IntelliMove(options2,weights)
        choose = rand.choice(options2)
    else:
        return "No such team"

    move(board, choose[0],choose[1],choose[2],choose[3])

#MakeBoard = sets the board up in terms of 1, -1, 0, and null
#MakeBoard: Initializes the board with the starting configuration. It sets the board variable to a list of 64 integers representing 
# the squares of the board. It then sets the values of the squares to 1, -1, or 0, depending on their position on the board.
def MakeBoard():
    global board
    for instances in range(0,64):
        board.append(0)

    for x in range(len(board)):
        #Every other square i na row, alternating which row starts w/ one, and not in the middle yet
        if (x + (x // 8)) % 2 == 0:
            board[x] = 0
        if (x + (x // 8)) % 2 == 0 and x < 24: #x < 24 is usual
            board[x] = 1
        if (x + (x // 8)) % 2 == 0 and x > 40: #x > 40 is usual
            board[x] = -1
        if (x + (x // 8)) % 2 == 1:
            board[x] = 'null'

#CanMove = returns true if an active square has at least one movement
#CanMove: Checks if any piece on the board can make a move. It takes the board as a parameter and returns two lists of tuples - 
#options1 and options2 - representing the possible moves for teams 1 and -1 respectively.
def CanMove(board):
    global options1, options2
    options1 = []
    options2 = []
    for index in range(len(board)):
        #For every square that isn't 0 or null
        if board[index] != 0 and board[index] != 'null':
            team = board[index]
            if (56 < index <= 63 and board[index] == 1) or (0 <= index < 8 and board[index] == -1):
                board[index] = 2 * board[index]
            #For every direction it can move
            for dire in direc:
                dire = direc[dire]
                newind = index + dire
                skipind = index + 2 * dire

                if (-1 < newind <= 63 and not ((board[newind] == team * -1 or board[newind] == team * -2 or board[newind] == team * -.5) and not -1 < skipind < 64)):
                    #Index of newind, if there's a faulty jump
                    if not(((board[newind] == team * -1 or board[newind] == team * -2 or board[newind] == team * -.5) and -1 < skipind < 64 and board[skipind] != 0) or board[newind] == team or board[newind] == team * 2 or board[newind] == team * .5 or (abs((index // 8)-(newind // 8)) != 1)) :
                        #Above checks- Faulty Skip Logic, the same teams piece in newind, and jumping more than one line 
                        if not (dire * team < 0 and not abs(board[index]) // 2 == 1):
                            #if it's not moving "Backwards" or it's a king
                            if board[index] > 0:
                                #Team 1
                                options1.append((index, dire, board[index], board[newind]))
                            elif board[index] < 0:
                                #Team 2
                                options2.append((index, dire, board[index], board[newind]))
    return options1, options2

#PrintStats = the print statements at the end
# winlist calculates the percentage of wins for each team 
def PrintStats():
    global totaltime

    pclock.tick()
    totaltime += pclock.get_time() / 1000
    gamesran = len(winlist)
    if len(winlist) > 0:
        print()
        print("Game stats: " + str(gamesran) + " games ran in" + " %2d hours, %2d minutes, %2.2f seconds" %(totaltime//3600, (totaltime%3600)//60, totaltime%60) + ", avg time(s) per game = %2.2f" % (totaltime / gamesran))
        print("Team 1 wins: " + str(winlist.count(1)) + ", Percentage = %2.2f" % ((winlist.count(1)/len(winlist))*100))
        print("Team 2 wins: " + str(winlist.count(-1)) + ", Percentage = %2.2f" % ((winlist.count(-1)/len(winlist))*100))
        print()
    else:
        print()
        print("Game stats: " + str(gamesran) + " games ran in" + " %2d hours, %2d minutes, %2.2f seconds" %(totaltime//3600, (totaltime%3600)//60, totaltime%60))
        print()

    if len(winlist) % sqlUpdate_after_NGames == 0 and len(winlist) > 0:
        Updatesqldb()

#Updatesqldb = Stores and then clears the data, so it runs fast always. No need to restart

#Updatesqldb() calls the run() method from a sqlm object, which is not defined in the code snippet you provided. 
# It's likely that sqlm is an instance of a class that encapsulates a SQL database and provides methods for updating the database. 
# Without knowing more about the class and its methods, it's impossible to say what Updatesqldb() does specifically, 
# but it likely updates the SQL database with data from the program.
def Updatesqldb():
    sqlm.run()

#UserMove = Checks where the users cursor clicks to move that piece to the next square

#UserMove(game) is a function that defines the behavior of the user's moves in the game. It takes a game object as an argument, 
# which is an instance of the Game class. The function first updates the game's events and pieces, and then determines 
# where the user's cursor is on the board by calling pygame.mouse.get_pos(). It then checks which squares are valid moves for 
# the current piece by iterating through the options2 list, which likely contains information about the available moves for each piece. 
# If the user clicks on a valid square, the function moves the piece to that square and returns. If the user clicks the right mouse button,
#  the function resets the square variable to None. The function also calls UpdateScreen() to update the display.
def UserMove(game):
    global square
    screen = game.screen
    size = game.size

    while game.running:
        game.gameEvent()
        game.PieceUpdate()

        mouse = pygame.mouse.get_pos()
        mx = mouse[0] // 50
        my = mouse[1] // 50

        choices = []
        optionlist = []
        for option in options2:
            if option[0] == square:
                choice=(square + option[1] + option[1]*(abs(option[3]) % 2))
                choices.append(choice)
                optionlist.append(option)
                pygame.draw.rect(screen, (200,200,200,128), ((choice%8)*size, (choice//8)*size, size, size))

            click = pygame.mouse.get_pressed()
        
        #return t or f, if move successful t, break
        if click[0] == 1:
            square = (my * 8) + mx
            if square in choices:
                option = optionlist[choices.index(square)]
                square = None
                move(board,option[0],option[1],option[2],option[3])
                return

        if click[2] == 1:
            square = None
        
        UpdateScreen()

    #if square:
        #pygame.draw.rect(screen, (200,200,200,128), ((square%8)*size, (square//8)*size, size, size))

    #Side note, the allow logic just see if the move it's trying to do is in options
    #Just highlight all in options and click one of the options. Fact check if its bad square




#run() is the main game loop that updates the game state and calls the other functions. It initializes the Game object and the MCTS object,
#  sets up the Pygame window, and begins the main loop. On each iteration of the loop, the function updates the game's events and pieces, 
#  calls CanMove() to calculate the valid moves for the current player, and uses MCTS to choose the next move. 
# It then updates the game's state and checks if the game is over. Finally, the function updates the display and 
# prints various statistics about the game. At the end of the game, it calls PrintStats() to print the winner, 
# and then closes the MCTS object.
def run():
    global board, totaltime
    game = Game(400)
    pygame.init()
    game.init()
    tree = MCTS()

    #pclock counts the entire game time
    pclock.tick()

    while (game.running):
        game.gameEvent()

        if len(options1) > 0:

            #print('IF options1')
            
            board_state = Board_State(board)
            best_move = get_best_moveBlue(board_state, 3)
            board = (best_move.board)
            CanMove(board)

        
        if len(options2) > 0:
            #CompMove(-1)
            UserMove(game)
            

        #print('ELIFoptions2')
        
        #board_state = Board_State(board)
            # this is calling the minimax.get_best_move() function 
         
        #    best_move = get_best_moveABPruning(board_state, 10)
            
        #    board = (best_move.board)

            # Assuming you have a Board_State instance called 'current_board'
            

            
        #    CanMove(board)
   
            

        if len(options1) <= 0 or len(options2) <= 0:
            game.Restart()

        pclock.tick()
        totaltime += pclock.get_time() / 1000
        game.PieceUpdate() #These two lines update the visual part
        UpdateScreen() #Removing them makes it run faster

    pygame.quit()
    PrintStats() # prints who team wins at the end of each game 
    tree.close()



def create_table():
    connection = sql.connect("MoveData.db")
    crsr = connection.cursor()

 # Create the data table if it doesn't exist
    crsr.execute('''CREATE TABLE IF NOT EXISTS data 
                (board TEXT PRIMARY KEY, n INTEGER DEFAULT 0, q FLOAT DEFAULT 0.0, avgR FLOAT DEFAULT 0.0)''')

# Create the data2 table if it doesn't exist
    crsr.execute('''CREATE TABLE IF NOT EXISTS data2 
                (board TEXT PRIMARY KEY, n INTEGER DEFAULT 0, q FLOAT DEFAULT 0.0, avgR FLOAT DEFAULT 0.0)''')


    connection.commit()
    connection.close()

create_table()
run()  




