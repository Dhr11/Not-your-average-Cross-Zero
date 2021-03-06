#!/usr/bin/env python3


import pygame
from math import floor
import game_engine as engine
import wrap_sentences as wraps
#import multiprocessing
from subprocess import STDOUT, check_output, Popen, PIPE, TimeoutExpired

XO   = "x"   # turn player
grid = []
for i in range(0, 8):
        bd = []
        for j in range(0, 5):
            bd.append('.')
        grid.append(bd)
winner = None


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,width,height,ic,ac,action=None):
    mouse_x,mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+width > mouse_x > x and y+height > mouse_y > y:
        pygame.draw.rect(ttt, ac,(x,y,width,height))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(ttt, ic,(x,y,width,height))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    ttt.blit(textSurf, textRect)



# declare our support functions

def initBoard(ttt):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    # ttt : a properly initialized pyGame display variable

    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))

    # draw the grid lines
    # vertical lines...
    for i in range (100,500,100):
        pygame.draw.line (background, (0,0,0), (i, 0), (i, 560), 2)
        pygame.draw.line (background, (0,0,0), (0, 0.7*i), (500, 0.7*i), 2)
    for i in range (500,800,100):
        pygame.draw.line (background, (0,0,0), (0, 0.7*i), (500, 0.7*i), 2)
    pygame.draw.line (background, red, (0, 350), (500, 350), 20)
    return background

def display_col(board):
    global col_selected
    pygame.draw.line (board, wheat1, (100*col_selected+50, 0), (100*col_selected+50, 500), 50)    
def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board

    global XO, winner

    # determine the status message
    if (winner is None):
        message = XO + "'s turn"
    else:
        message = winner + " won!"
        
    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill ((250, 250, 250), (0, 650, 300, 25))
    board.blit(text, (10, 650))

def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    button("Rotate",600,350,100,50,green,bright_green,lambda: rot_ui(board))
    button("Drop",600,450,100,50,green,bright_green,lambda: drop_ui(board))
    pygame.display.flip()
    
def boardPos (mouseX, mouseY):
    # mouseX : the X coordinate the user clicked
    # mouseY : the Y coordinate the user clicked

    # determine the row the user clicked
    row = floor(mouseY/100) if mouseY  <500 else 4
    col = floor(mouseX/100) if mouseX  <500 else 4
    # return the tuple containg the row & column
    return (row, col)

def drawMove (board, boardRow, boardCol, Piece):

    #print("draw ",Piece)
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 70) + 35

    # draw the appropriate piece
    if (Piece == 'o'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 30, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 20, centerY - 20), \
                         (centerX + 20, centerY + 20), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 20, centerY - 20), \
                         (centerX - 20, centerY + 20), 2)

    # mark the space as used
    #grid [boardRow][boardCol] = Piece
def drop_ui(board):
    global grid,col_selected
    global XO
    
    for r in range(7,-1,-1):
        if grid[r][col_selected] =="." : 
            grid[r][col_selected] = XO
            drawMove(board,r,col_selected,XO)
            if (XO == "x"): XO = "o"
            else:   XO = "x"
            break

rotated = 0     

def rot_ui(board):
    global grid,rotated,col_selected
    global XO
    grid = engine.rotate(col_selected,grid)
    if (XO == "x"): XO = "o"
    else:   XO = "x"
    rotated = 1

def board_change(board):
    global rotated
    
    board = initBoard (ttt)
    ttt.fill(white)
    ttt.blit (board, (0, 0))
    pygame.draw.line (board, wheat1, (100*col_selected+50, 0), (100*col_selected+50, 560), 50)
    [drawMove(board,r,c,grid[r][c]) for r in range(0,8) for c in range(0,5) if grid[r][c] is not "."]
    
    rotated =0
    return board

col_selected = 0
def clickBoard(board):
    # determine where the user clicked and if the space is not already
    # occupied, draw the appropriate piece there (X or O)
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, XO, col_selected,rotated
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    if(mouseX>500 or mouseY>560):   return
    (row, col) = boardPos (mouseX, mouseY)
    col_selected = col
    rotated = 1
    # make sure no one's used this space
    if ((grid[row][col] == "x") or (grid[row][col] == "o")):
        # this space is in use
        return
    
    """
    # draw an X or O
    drawMove (board, row, col, XO)    ###check edit remove draw move if outside area

    # toggle XO to the other player's move
    if (XO == "x"): XO = "o"
    else:   XO = "x"
    """
    
def Oturn(board):
    global XO, grid , rotated
    if XO=='o':
        #output = check_output('python game_engine.py 5 o '+engine.boardstring(grid)+' 5', stderr=STDOUT, timeout=4)
        CREATE_NO_WINDOW = 0x08000000
        
        proc = Popen(['python','game_engine.py','5' ,'o',engine.boardstring(grid),'1'], stdout=PIPE, stderr=STDOUT,creationflags=CREATE_NO_WINDOW)
        #print(proc.stdout(timeout=4)[0])
        #print((str(proc.communicate()[0]).split()[-1]).split('\\')[0])
        grid = engine.stringboard((str(proc.communicate()[0]).split()[-1]).split('\\')[0],5)
        rotated =1
        XO='x'
        
    pass    
def gameWon(board):
    # determine if anyone has won the game
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, winner

    # check for winning rows
    for row in range (0, 5):
        if ((grid [row][0] == grid[row][1] == grid[row][2]==grid[row][3]==grid[row][4]) and \
           (grid [row][0] is not ".")):
            # this row won
            winner = grid[row][0]
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*70 - 35), \
                              (500, (row + 1)*70 - 35), 2)
            break

    # check for winning columns
    for col in range (0, 5):
        if (grid[0][col] == grid[1][col] == grid[2][col]== grid[3][col]== grid[4][col]) and \
           (grid[0][col] is not "."):
            # this column won
            winner = grid[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                              ((col + 1)* 100 - 50, 315), 2)
            break

    # check for diagonal winners
    if (grid[0][0] == grid[1][1] == grid[2][2]== grid[3][3]== grid[4][4]) and \
       (grid[0][0] is not "."):
        # game won diagonally left to right
        winner = grid[0][0]
        pygame.draw.line (board, red, (50, 35), (450, 315), 2)

    if (grid[0][4] == grid[1][3] == grid[2][2]== grid[3][1]== grid[4][0]) and \
       (grid[0][4] is not "."):
        # game won diagonally right to left
        winner = grid[0][4]
        pygame.draw.line (board, (250,0,0), (50, 315), (450, 35), 2)


def game_main():
    # create the game board
    board = initBoard (ttt)
    
    # main event loop
    running = 1
    
    while (running == 1):
        for event in pygame.event.get():
            
            if event.type is pygame.QUIT:
                running = 0
            elif event.type is pygame.MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                clickBoard(board)
            #display_col(board)    
            # check for a winner
            
            gameWon (board)
            showBoard (ttt, board)
            Oturn(board)
            #
            if rotated==1: board = board_change(board)
            # update the display
            
            
            #print(grid)          

def intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        ttt.fill(white)
        largeText = pygame.font.SysFont("comicsansms",35)
        TextSurf, TextRect = text_objects("Betsy - Modern Tic tac toe", largeText)
        TextRect.center = ((display_width/3),(display_height/8))
        ttt.blit(TextSurf, TextRect)

        my_string = """           Rules/Modifications  
            1. In the 8x5 grid, aim is to win by completing a line of X's in 5 cells. The bottom marked 3 region is not counted. 
            2. You can win by having a line of 5 X's in row column or diaganol
            3. Instead of placing X's, you have to select a column by clicking it, thus highlighting it, then click on drop to drop the X in the empty space in that column
            4. You can also rotate the column in you r turn instead of dropping. Rotate, rotates the column down"""
        my_rect = pygame.Rect((40, 200, 600, 300))
        instText = pygame.font.SysFont("comicsansms",15)
        
        rendered_text = wraps.render_textrect(my_string, instText, my_rect, (48, 48, 48), (216, 216, 216), 0)

        
        #TextSurfinst, TextRectinst = text_objects(, instText)
        #TextRectinst.center = ((display_width/2),(display_height/4))
        ttt.blit(rendered_text, my_rect.topleft)
        
        button("GO!",150,600,100,50,green,bright_green,game_main)
        #button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        



# --------------------------------------------------------------------
# initialize pygame and our window
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
bright_red = (127,0,0)
green = (0,255,0)
bright_green = (0,127,0)
wheat1 = (255,231,186)
display_height = 800
display_width = 800

pygame.init()
size = [700,700] #300 325 initial
ttt = pygame.display.set_mode (size)
pygame.display.set_caption ('Not your average Cross-Zero')

intro()