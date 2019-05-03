print("CMPT103-18S_Icebreaker_CJ 12/6/2018 John Chubey  Milestone #3")

"""
CMPT103-18S_Icebreaker_CJ 12/6/2018 John Chubey  Milestone #3
Date: May 27, 2018
Author: John Chubey

Description: In the first milestone a board is created in a window with an 
array of squares of all the potential moves. Quit and Reset buttons are created
and are responsive, as well as a text output displaying the flow of the game,
as well as the actions that have just been taken.

In the second milestone each square is interactive, however only on the proper 
player's turn. The player is limited to only moving to squares adjacent to them.
Also, the player is prevented from moving to any square that is broken (blue) or
occupied by the other player. The Text display is updated based on who's move it
is and what stage of their turn they're on (move or break squares). A separate
file was created to hold the custom classes required by the game, called 
icebreaker_classes_CJ.py.

In the third and final milestone, the game is complete. A splash screen is 
created when the window initially loads up, and the board doesn't load until the
"Play game" button is pressed. Once pressed, the splash screen is wiped and 
the game board loads. The end of game is detected correctly from all possibilities
(trapped by player, trapped against the side of the board, surrounded by broken
squares). The game then closes after the player has won or a draw is reached.

"""

#--------------------------------------------------------------------------
# Imports:
from graphics import *
from icebreaker_classes_CJ import *

#--------------------------------------------------------------------------
# Global Variables

WINDOW_W = 610 # Window Width.
WINDOW_H = 800 # Window Height.

BOARD_START_X = 10 # Starting x value for the board in the window.
BOARD_START_Y = 10 # Starting y value for the board in the window.

BOX_SIDE = 50 # Length of each size of each respective box.
BOX_COLOR = "white" # Background color for all boxes.

#--------------------------------------------------------------------------
# Helper Functions

def build_board(win, base_x, base_y):
    """
    Description: Build a board of boxes that represent potential moves by the 
    players.
    Inputs: 
    win (GraphWin) - The main window object used to display objects on the 
    screen.
    base_x (int) - An integer value representing the x value of the starting
    point on the board.
    base_y (int) - An integer value representing the y value of the starting
    point on the board.
    Outputs: 
    board (list) - A two dimensional list representing the board.
    """
    board = []
    cur_pt = Point(base_x, base_y)
    for i in range(0, 10):
        row = []
        for j in range(0, 10):
            rect = Rectangle(Point(cur_pt.x, cur_pt.y),\
                             Point(cur_pt.x + BOX_SIDE, cur_pt.y + BOX_SIDE))
            rect.setFill(BOX_COLOR)
            rect.draw(win)
            row.append(rect)
            cur_pt.x += (BOX_SIDE + 10)
        cur_pt.y += (BOX_SIDE + 10)
        cur_pt.x = base_x
        board.append(row)
    
    return board
    

def build_buttons(win, end_of_boxes):
    """
    Description: Build the Quit and Reset buttons and place them in the window.
    Inputs: 
    win (GraphWin) - The main window object used to display objects on the 
    screen.
    end_of_boxes (int) - The y value of the end of the boxes on the screen.
    Outputs: 
    quit_rect (Rectangle) - A rectangle object representing the area of the 
    Quit button.
    reset_rect (Rectangle) - A rectangle object representing the area of the 
    Reset button.
    """    
    buttons_base_pt = Point(WINDOW_W - 70, end_of_boxes + 30)
    quit_rect = Rectangle(buttons_base_pt,\
                          Point(buttons_base_pt.x + 60, buttons_base_pt.y + 35))
    quit_rect.draw(win)
    quit_text = Text(Point(buttons_base_pt.x + 30, buttons_base_pt.y + 17),\
                     "QUIT")
    quit_text.draw(win)
    
    reset_rect = Rectangle(Point(buttons_base_pt.x, buttons_base_pt.y + 45),\
                           Point(buttons_base_pt.x + 60, buttons_base_pt.y + 80))
    reset_rect.draw(win)
    reset_text = Text(Point(buttons_base_pt.x + 30, buttons_base_pt.y + 62),\
                      "RESET")
    reset_text.draw(win)
    
    return quit_rect, reset_rect
    
    
    
def in_Rectangle(pt, rect):
    """
    Description: Check if a given point is in a given Rectangle.
    Inputs: 
    pt (Point) - A point to be checked.
    rect (Rectangle) - A rectangle used to check if the pt is inside.
    Outputs: 
    Boolean - A true of false statement of whether the point is inside the 
    rectangle.
    """    
    return  rect.getP1().x <= pt.getX() <= rect.getP2().x and\
            rect.getP1().y <= pt.getY() <= rect.getP2().y 

def get_box_center(rect):
    """
    Description: Find the center of a given Rectangle.
    Inputs: 
    rect (Rectangle) - The desired Rectangle who's center is required.
    Outputs: 
    (Point) - A point object representing the center of the rectangle.
    """    
    return Point(rect.getP1().x + BOX_SIDE // 2, rect.getP1().y + BOX_SIDE // 2)

    
def splash_screen(win, screen_W, screen_H):
    """
    Description: Display a splash screen when the window is loaded.
    Inputs: win (GraphWin) - The current window object.
            screen_W (int) - The screen width.
            screen_H (int) - The screen height.
    Output: None.
    """
    splash_text = Text(Point(screen_W//2, screen_H//2),\
                       "Welcome to Icebreaker!\n\n Created by John Chubey\n\n" +\
                       " Press the button to start!") 
    
    splash_text.draw(win)
    
    splash_btn_base_pt = Point(screen_W//2 - 50, screen_H//2 + 70)
    start_rect = Rectangle(splash_btn_base_pt,\
                          Point(splash_btn_base_pt.x + 100, splash_btn_base_pt.y + 70))
    start_rect.draw(win)
    start_text = Text(Point(splash_btn_base_pt.x + 50, splash_btn_base_pt.y + 35),\
                     "Play game!")
    start_text.draw(win)    
    
    splash_objects = [splash_text, start_rect, start_text]
    while True:
        splash_click = win.getMouse()
        if in_Rectangle(splash_click, start_rect):
            for obj in splash_objects:
                obj.undraw()
            
            break 
    
#--------------------------------------------------------------------------

def main():
    """
    Description:  The main function that runs the program if this file is run
    as the main file. Most of the high level game logic is housed in the main 
    function.
    Inputs: None.
    Outputs: None.
    """
    win = GraphWin("Name: John Chubey,    Project name: Icebreaker,   " + \
                   "Date: 12/6/2018,    Version: 1.03", WINDOW_W, WINDOW_H)
    
    splash_screen(win, WINDOW_W, WINDOW_H)
    
    players = ["red", "blue"]
    cur_player = "red"
    quit_btn_pressed = False    
    
    end_of_boxes = BOARD_START_Y + (10 * (BOX_SIDE + 10))
    text_midpoint = Point(WINDOW_W // 2, end_of_boxes +\
                           (WINDOW_H - end_of_boxes) // 2)
    
    main_text = Text(text_midpoint, "Ice Breaker!")
    main_text.draw(win)
    
    quit_btn, reset_btn = build_buttons(win, end_of_boxes)
    
    game_board_list = build_board(win, BOARD_START_X, BOARD_START_Y)
    gameBoard = GameBoard(win, game_board_list)
    
      
    
    while True:
        reset_btn_pressed = False
        main_text.setText("It's " + cur_player.capitalize() + "'s turn to move!")
        click = win.getMouse()
        
        if gameBoard.clicked(click) and gameBoard.valid_move(click, cur_player):
            gameBoard.move_player(cur_player, gameBoard.clicked_square(click))
            
            while True:
                main_text.setText("It's " + cur_player.capitalize() +\
                                  "'s turn to break ice!")
                icebreak_click = win.getMouse()
                if gameBoard.clicked(icebreak_click) and\
                   gameBoard.valid_iceBreak(icebreak_click):
                    gameBoard.break_ice(icebreak_click)
                    cur_player = players[cur_player == "red"]
                    break
                elif in_Rectangle(icebreak_click, quit_btn):
                    quit_btn_pressed = True
                    break
                elif in_Rectangle(icebreak_click, reset_btn):
                    reset_btn_pressed = True
                    break
        
        if in_Rectangle(click, quit_btn) or quit_btn_pressed:
            main_text.setText("Thanks for playing Ice Breaker! Goodbye!")
            break
        if in_Rectangle(click, reset_btn) or reset_btn_pressed:
            main_text.setText("Game Reset!\n Click to start!")
            gameBoard.reset()
            cur_player = players[0]
            win.getMouse()
            
        if gameBoard.game_over():
            if gameBoard.winner().lower() == "draw":
                main_text.setText("The game is a draw!!")
            else:
                main_text.setText(gameBoard.winner() + " has won the game!!")
            win.getMouse()
            main_text.setText("Thanks for playing Ice Breaker! Goodbye!")
            break
    
    
    
    
    
    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()