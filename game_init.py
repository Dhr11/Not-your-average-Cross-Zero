#!/usr/bin/python


# import necessary modules
import pygame
from math import floor
import game_engine as engine
#from pygame.locals import *

# declare our global variables for the game
XO   = "x"   # track whose turn it is; X goes first
grid = []
for i in range(0, 5):
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
        pygame.draw.line (background, (0,0,0), (i, 0), (i, 500), 2)
        pygame.draw.line (background, (0,0,0), (0, i), (500, i), 2)
    #pygame.draw.line (background, wheat1, (0, 0), (0, 500), 20)
    # return the board
    return background

def display_col(board):
    global col_selected
    pygame.draw.line (board, wheat1, (100*col_selected+50, 0), (100*col_selected+50, 500), 50)    
def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board
    # ---------------------------------------------------------------
    # board : the initialized game board surface where the status will
    #         be drawn

    # gain access to global variables
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
    board.fill ((250, 250, 250), (0, 600, 300, 25))
    board.blit(text, (10, 600))

def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    button("Rotate",650,350,100,50,green,bright_green,lambda: rot_ui(board))
    button("Drop",650,450,100,50,green,bright_green,lambda: drop_ui(board))
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

    print("draw ",Piece)
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    # draw the appropriate piece
    if (Piece == 'o'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 44, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 25, centerY - 25), \
                         (centerX + 25, centerY + 25), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 25, centerY - 25), \
                         (centerX - 25, centerY + 25), 2)

    # mark the space as used
    #grid [boardRow][boardCol] = Piece
i=0
def drop_ui(board):
    global i
    i+=1
    print(i)
    global grid,col_selected
    global XO
    
    for r in range(4,-1,-1):
        if grid[r][col_selected] =="." : 
            grid[r][col_selected] = XO
            drawMove(board,r,col_selected,XO)
            if (XO == "x"): XO = "o"
            else:   XO = "x"
            break
    """
    print("new board start")
    board = initBoard (ttt)
    ttt.blit (board, (0, 0))
    pygame.display.flip()
    print(grid," dsds")
    
    print("befpre new grid")
    
    grid = engine.drop(0,XO,grid)
    print(grid)
    if (XO == "x"): XO = "o"
    else:   XO = "x"
    print("new board print start")
    [drawMove(board,grid.index(i),i.index(a),a) for i in grid for a in i if a is not "_"]
    print("new board done")
    """
rotated = 0     
def rot_ui(board):
    global grid,rotated,col_selected
    global XO
    print("new board start")
    
    print(grid," dsds")
    
    print("before new grid")
    
    grid = engine.rotate(col_selected,grid)
    print(grid)
    if (XO == "x"): XO = "o"
    else:   XO = "x"
    print("new board print start")
    rotated = 1
    """
    board = initBoard (ttt)
    ttt.fill(white)
    ttt.blit (board, (0, 0))
    #pygame.display.update()
    pygame.display.update()
    [drawMove(board,grid.index(i),i.index(a),a) for i in grid for a in i if a is not "."]
    pygame.display.update()
    print("new board done")
    """
def board_change(board):
    global rotated
    
    board = initBoard (ttt)
    ttt.fill(white)
    ttt.blit (board, (0, 0))
    pygame.draw.line (board, wheat1, (100*col_selected+50, 0), (100*col_selected+50, 500), 50)
    [drawMove(board,r,c,grid[r][c]) for r in range(0,5) for c in range(0,5) if grid[r][c] is not "."]
    
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
    if(mouseX>500 or mouseY>500):   return
    (row, col) = boardPos (mouseX, mouseY)
    col_selected = col
    rotated = 1
    # make sure no one's used this space
    if ((grid[row][col] == "x") or (grid[row][col] == "o")):
        # this space is in use
        return
    
    #board.fill (wheat1, (0, 100, 100, 100))
    #highlight = pygame.Surface((100, 100))
    #highlight.fill(wheat1)
    #board.blit((0,0),(0,100,100,100))
    """
    # draw an X or O
    drawMove (board, row, col, XO)    ###check edit remove draw move if outside area

    # toggle XO to the other player's move
    if (XO == "x"): XO = "o"
    else:   XO = "x"
    """
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
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), \
                              (500, (row + 1)*100 - 50), 2)
            break

    # check for winning columns
    for col in range (0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]== grid[3][col]== grid[4][col]) and \
           (grid[0][col] is not "."):
            # this column won
            winner = grid[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                              ((col + 1)* 100 - 50, 500), 2)
            break

    # check for diagonal winners
    if (grid[0][0] == grid[1][1] == grid[2][2]== grid[3][3]== grid[4][4]) and \
       (grid[0][0] is not "."):
        # game won diagonally left to right
        winner = grid[0][0]
        pygame.draw.line (board, (250,0,0), (50, 50), (450, 450), 2)

    if (grid[0][4] == grid[1][3] == grid[2][2]== grid[3][1]== grid[4][0]) and \
       (grid[0][4] is not "."):
        # game won diagonally right to left
        winner = grid[0][4]
        pygame.draw.line (board, (250,0,0), (450, 50), (50, 450), 2)


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
            
            #
            if rotated==1: board = board_change(board)
            # update the display
            
            showBoard (ttt, board)# -*- coding: utf-8 -*-
            print(grid)          

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
        TextSurf, TextRect = text_objects("Betsy - Tic tac toe for adults", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        ttt.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_main)
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
size = [800,800] #300 325 initial
ttt = pygame.display.set_mode (size)
pygame.display.set_caption ('Not your average Cross-Zero')

intro()