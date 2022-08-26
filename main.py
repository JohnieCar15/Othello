#!/usr/bin/env python3

import pygame, sys
import math
 
pygame.init()
 
WIDTH, HEIGHT = 900, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption("Tic Tac Toe!")
 
BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")
 
BG_COLOR = (214, 201, 227)
 
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]]
 
to_move = 'X'
 
SCREEN.fill(BG_COLOR)
SCREEN.blit(pygame.transform.scale(BOARD, (WIDTH, HEIGHT)), (0, 0))
 
pygame.display.update()

def render_board(size, board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*(size[1] / 3)+(size[1] / 6), i*(size[0] / 3)+(size[0] / 6)))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*(size[1] / 3)+(size[1] / 6), i*(size[0] / 3)+(size[0] / 6)))




def adjust_mouse_pos(size, board, graphical_board, to_move):
    coordinates = pygame.mouse.get_pos()
    x_pos = math.floor(coordinates[0] / (size[0] / 3))
    y_pos = math.floor(coordinates[1] / (size[1] / 3))
    if board[y_pos][x_pos] != "O" and board[y_pos][x_pos] != "X":
        board[y_pos][x_pos] = to_move
        if to_move == "X":
            to_move = "O" 
        else: 
            to_move = "X"


    render_board(size, board, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board, to_move

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode(event.size, flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
            SCREEN.fill(BG_COLOR)
            SCREEN.blit(pygame.transform.scale(BOARD, event.size), (0, 0))
            render_board(pygame.display.get_surface().get_size(), board, X_IMG, O_IMG)
            print(graphical_board)
            for i in range(3):
                for j in range(3):
                    if graphical_board[i][j][0] is not None:
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board, to_move = adjust_mouse_pos(pygame.display.get_surface().get_size(), board, graphical_board, to_move)
            pygame.display.update()
            
