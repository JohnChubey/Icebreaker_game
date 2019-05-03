"""
Description: This is a support/class file for 'icebreaker_CJ.py'.
"""
#--------------------------------------------------------------------------
# Imports:
from icebreaker_CJ import *
from graphics import *

#--------------------------------------------------------------------------
# Classes:

class GameBoard():
    """
    Description: An object representing the Icebreaker game board.
    Inherited classes: None.
    """    
    def __init__(self, win, gameBoardList):
        """
        Description: Construct the GameBoard object.
        Inputs: self (GameBoard) - The current GameBoard object.
                win (GraphWin) - The window displaying the game.
                gameBoardList (List) - A two dimensional list of Rectangles,
                representing the spaces on the board.
        Outputs: None.
        """
        self.win = win
        self.gameBoardList = gameBoardList
        self.redPlayer = Player(self.win, self.gameBoardList, "RED", [4, 0])
        self.bluePlayer = Player(self.win, self.gameBoardList, "BLUE", [4, 9])
        
    def valid_move(self, click, player):
        """
        Description: Check if the user's move is valid.
        Inputs: self (GameBoard) - The current GameBoard object.
                click (Point) - A point object of the spot where the user clicked.
                player (Player) - The current player.
        
        Outputs: A boolean value of True or False.
        """        
        if player.lower() == "red":
            cur_player = self.redPlayer
        else:
            cur_player = self.bluePlayer
        row_col = self.clicked_square(click)
        clicked_square = self.gameBoardList[row_col[0]][row_col[1]]
        return not row_col == self.redPlayer.get_pos() and\
               not row_col == self.bluePlayer.get_pos() and\
               cur_player.is_adjacent(row_col)\
               and self.not_broken(row_col)

    def move_player(self, player, new_pos):
        """
        Description: Determind which player's move it is and move 
        that player to a new game space.
        Inputs: self (GameBoard) - The current GameBoard object.
                player (Player) - The current player.
                new_pos (List) - A list of length 2 containing the new game 
                space to be moved to.
        Outputs: None.
        """        
        if player.lower() == "red":
            cur_player = self.redPlayer
        else:
            cur_player = self.bluePlayer
        
        cur_player.move(new_pos)
        
    def not_broken(self, row_col):
        """
        Description: Check if the game space is not broken.
        Inputs: self (GameBoard) - The current GameBoard object.
                row_col (List) - A list of length 2 containing the game space
                to be checked.
        Outputs: A boolean value.
        """        
        clicked_square = self.gameBoardList[row_col[0]][row_col[1]]
        return clicked_square.config["fill"].lower() == BOX_COLOR
        
        
    
    def clicked(self, click):
        """
        Description: Check if the GameBoard was clicked.
        Inputs: self (GameBoard) - The current GameBoard object.
                click (Point) - The point where the user clicked in the window.
        Outputs: A boolean value.
        """        
        for row in self.gameBoardList:
            for square in row:
                if in_Rectangle(click, square):
                    return True
    
        return False 
    
    def clicked_square(self, click):
        """
        Description: Return the GameBoard coordinates of a clicked game space.
        Inputs: self (GameBoard) - The current GameBoard object.
                click (Point) - The point where the user clicked in the window.
        Outputs: (List) a list of length 2 representing the row and column, 
        repectively, of the clicked game space.
        """        
        for i in range(len(self.gameBoardList)):
            for j in range(len(self.gameBoardList[i])):
                if in_Rectangle(click, self.gameBoardList[i][j]):
                    return [i, j]
    
    def valid_iceBreak(self, click):
        """
        Description: Check if the game spaced clicked is valid to break.
        Inputs: self (GameBoard) - The current GameBoard object.
                click (Point) - The point where the user clicked in the window.
        Outputs: A boolean value.
        """        
        row_col = self.clicked_square(click)
        clicked_square = self.gameBoardList[row_col[0]][row_col[1]]
        
        return clicked_square.config["fill"].lower() == BOX_COLOR and\
               not row_col == self.redPlayer.get_pos() and\
               not row_col == self.bluePlayer.get_pos()
    
    def break_ice(self, click):
        """
        Description: Break a block of ice.
        Inputs: self (GameBoard) - The current GameBoard object.
                click (Point) - The point where the user clicked in the window.
        Outputs: None.
        """        
        row_col = self.clicked_square(click)
        clicked_square = self.gameBoardList[row_col[0]][row_col[1]]
        clicked_square.setFill("blue")

    def reset(self):
        """
        Description: Reset the game board to it's initial state.
        Inputs: self (GameBoard) - The current GameBoard object.
        Outputs: None.
        """        
        self.redPlayer.move([4, 0])
        self.bluePlayer.move([4, 9])
        for row in self.gameBoardList:
            for block in row:
                block.setFill(BOX_COLOR)
    
    def game_over(self):
        """
        Description: Check if the game is over (One player is surrounded).
        Inputs: None.
        Output: (bool) A boolean value of whether or not one of the players
        are trapped.
        """
        return self.redPlayer.is_trapped(self.bluePlayer) or\
               self.bluePlayer.is_trapped(self.redPlayer)
    
    def winner(self):
        """
        Description: Determine the winner of the game.
        Inputs: None.
        Output: (String) A string determining the outcome of the game.
        """        
        if self.bluePlayer.is_trapped(self.redPlayer) and\
           self.redPlayer.is_trapped(self.bluePlayer):
            return "Draw"
        elif self.bluePlayer.is_trapped(self.redPlayer):
            return "Red"
        else:
            return "Blue"
        
class Player():
    """
    Description: An object representing a player in Icebreaker.
    Inherited classes: None.
    """    
    def __init__(self, win, gameBoardList, color, startingPos):
        """
        Description: Construct a Player object.
        Inputs: self (Player) - The current Player object.
                win (GraphWin) - The window displaying the game.
                gameBoardList (List) - A two dimensional list of Rectangles,
                representing the spaces on the board.
                color (String) - The name of the player's color.
                startingPos (List) - A list of length 2 containing the game 
                space the player starts in.
        Outputs: None.
        """        
        self.win = win
        self.gameBoardList = gameBoardList        
        self.color = color
        self.cur_pos = startingPos
        self.playerCenter = Circle(get_box_center(\
            gameBoardList[startingPos[0]][startingPos[1]]), (BOX_SIDE//2) - 5)
        self.playerCenter.setFill(self.color)
        self.playerCenter.draw(self.win)
        
        
    
    def move(self, new_pos):
        """
        Description: Move the player to the new game space.
        Inputs: self (Player) - The current Player object.
                new_pos (List) - A list of length 2 containing the new game 
                space to be moved to.
        Outputs: None.
        """        
        self.playerCenter.undraw()
        self.cur_pos = new_pos
        self.playerCenter = Circle(get_box_center(\
            self.gameBoardList[new_pos[0]][new_pos[1]]), (BOX_SIDE // 2) - 5)
        self.playerCenter.setFill(self.color)
        self.playerCenter.draw(self.win)
    
    def is_adjacent(self, row_col):
        """
        Description: Check if a game space is adjacent to the player.
        Inputs: self (Player) - The current Player object.
                row_col (List) - A list of length 2 containing the game space
                to be checked.
        Outputs: A boolean value.
        """        
        return abs(row_col[0] - self.cur_pos[0]) <= 1 and\
               abs(row_col[1] - self.cur_pos[1]) <= 1
    
    def get_pos(self):
        """
        Description: Get the players current position on the game board.
        Inputs: self (Player) - The current Player object.
        Outputs: (List) A list of length 2 reprsenting the row and column of the
        player on the game board, respectively.
        """        
        return self.cur_pos
    
    def is_trapped(self, other_player):
        """
        Description: Check if the player is trapped.
        Inputs: other_player (Player) - The opposing player object.
        Output: (bool) A boolean value determining if the player is trapped or
        not.
        """        
        for i in range(-1,2):
            if self.cur_pos[0] + i < 0 or\
               self.cur_pos[0] + i > 9:
                continue
            for j in range(-1,2):
                if self.cur_pos[1] + j < 0 or\
                   self.cur_pos[1] + j > 9 or\
                   self.cur_pos == [self.cur_pos[0] + i, self.cur_pos[1] + j]:
                    continue
                square = self.gameBoardList[self.cur_pos[0] + i][self.cur_pos[1] + j]
                if square.config["fill"].lower() == BOX_COLOR and\
                   not [self.cur_pos[0] + i, self.cur_pos[1] + j] == other_player.get_pos():
                    return False
            
        return True
    
    
    
    
if __name__ == "__main__":
    print("The is a support file for 'icebreaker_CJ.py'. To run the game please "\
          + "run that file instead.")